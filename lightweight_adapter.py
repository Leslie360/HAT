"""Lightweight residual adapter with test-time training (TTT).

For each fresh analog instance:
  1. Freeze all pretrained backbone parameters
  2. Inject a small residual MLP adapter before the classifier head
  3. Fine-tune only the adapter on calibration set (20-50 SGD steps)
  4. Evaluate on test set

Why head-side:
  - All upstream block drift manifests in the final feature vector
  - Single adapter (not per-block) = minimal params, fast TTT
  - Residual connection preserves pretrained feature backbone
"""
from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class LightweightAdapter(nn.Module):
    """Residual MLP adapter: x -> x + fc2(act(fc1(x)))."""
    
    def __init__(self, dim: int, hidden_dim: int | None = None, dropout: float = 0.1):
        super().__init__()
        if hidden_dim is None:
            hidden_dim = max(dim // 4, 64)
        self.fc1 = nn.Linear(dim, hidden_dim)
        self.act = nn.GELU()
        self.dropout = nn.Dropout(dropout)
        self.fc2 = nn.Linear(hidden_dim, dim)
        self._init_weights()
    
    def _init_weights(self):
        nn.init.xavier_uniform_(self.fc1.weight)
        nn.init.zeros_(self.fc1.bias)
        nn.init.zeros_(self.fc2.weight)
        nn.init.zeros_(self.fc2.bias)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + self.dropout(self.fc2(self.act(self.fc1(x))))


def inject_adapter_before_head(model: nn.Module, hidden_dim: int | None = None, dropout: float = 0.1) -> nn.Module:
    """Inject LightweightAdapter into the model before classifier head.
    
    For Tiny-ViT NormMlpClassifierHead, the adapter is placed after flatten
    and before head.fc.
    """
    # Find the head module
    head = None
    for name, module in model.named_modules():
        if name == 'head':
            head = module
            break
    
    if head is None:
        raise ValueError("Model has no 'head' module")
    
    # Determine input dim to head.fc
    if hasattr(head, 'fc') and isinstance(head.fc, nn.Linear):
        dim = head.fc.in_features
    else:
        raise ValueError("Head module has no 'fc' Linear layer")
    
    adapter = LightweightAdapter(dim, hidden_dim=hidden_dim, dropout=dropout)
    
    # Monkey-patch head forward to include adapter
    original_forward = head.forward
    
    def new_forward(x):
        # Run original head logic up to fc
        x = head.global_pool(x)
        x = head.norm(x)
        x = head.flatten(x)
        x = head.pre_logits(x)
        x = head.drop(x)
        # Apply adapter
        x = adapter(x)
        # Final classification
        x = head.fc(x)
        return x
    
    head.forward = new_forward
    return adapter


def ttt_finetune_adapter(
    model: nn.Module,
    adapter: nn.Module,
    calib_loader: torch.utils.data.DataLoader,
    device: str,
    num_steps: int = 50,
    lr: float = 1e-3,
    weight_decay: float = 0.01,
) -> None:
    """Test-time training: fine-tune only the adapter on calibration set."""
    model.eval()
    
    # Freeze everything except adapter
    for param in model.parameters():
        param.requires_grad = False
    for param in adapter.parameters():
        param.requires_grad = True
    
    optimizer = torch.optim.AdamW(adapter.parameters(), lr=lr, weight_decay=weight_decay)
    criterion = nn.CrossEntropyLoss()
    
    adapter.train()
    for step in range(num_steps):
        total_loss = 0.0
        total_correct = 0
        total_samples = 0
        
        for images, labels in calib_loader:
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item() * images.size(0)
            total_correct += (outputs.argmax(dim=1) == labels).sum().item()
            total_samples += images.size(0)
        
        if step % 10 == 0 or step == num_steps - 1:
            avg_loss = total_loss / total_samples
            avg_acc = total_correct / total_samples * 100
            print(f"  TTT step {step:3d}/{num_steps}: loss={avg_loss:.4f} calib_acc={avg_acc:.2f}%")
    
    adapter.eval()


def remove_adapter_from_head(model: nn.Module) -> None:
    """Remove adapter and restore original head forward."""
    head = None
    for name, module in model.named_modules():
        if name == 'head':
            head = module
            break
    
    if head is None:
        return
    
    # Restore original forward if we saved it
    if hasattr(head, '_original_forward'):
        head.forward = head._original_forward
    # Otherwise, re-define clean forward
    else:
        def clean_forward(x):
            x = head.global_pool(x)
            x = head.norm(x)
            x = head.flatten(x)
            x = head.pre_logits(x)
            x = head.drop(x)
            x = head.fc(x)
            return x
        head.forward = clean_forward
