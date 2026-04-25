import torch
import unittest
import math
from analog_layers import StraightThroughQuantize

class TestSecondOrderSTE(unittest.TestCase):
    def test_ltp_second_order_acts_as_brake(self):
        x = torch.tensor([0.5], dtype=torch.float32, requires_grad=True)
        # LTP: grad_output < 0
        y = StraightThroughQuantize.apply(x, 16, 0.0, 1.0, 2.0, -2.0, None, True, 0.1, 1.0)
        y.backward(torch.tensor([-1.0]))
        grad_2nd = x.grad.item()
        
        x.grad.zero_()
        y_1st = StraightThroughQuantize.apply(x, 16, 0.0, 1.0, 2.0, -2.0, None, False, 0.0, 1.0)
        y_1st.backward(torch.tensor([-1.0]))
        grad_1st = x.grad.item()
        
        print(f"LTP 1st: {grad_1st}, 2nd: {grad_2nd}")
        self.assertTrue(abs(grad_2nd) < abs(grad_1st), "LTP 2nd order must be a brake")

    def test_ltd_second_order_acts_as_brake(self):
        x = torch.tensor([0.5], dtype=torch.float32, requires_grad=True)
        # LTD: grad_output > 0
        y = StraightThroughQuantize.apply(x, 16, 0.0, 1.0, 2.0, -2.0, None, True, 0.1, 1.0)
        y.backward(torch.tensor([1.0]))
        grad_2nd = x.grad.item()
        
        x.grad.zero_()
        y_1st = StraightThroughQuantize.apply(x, 16, 0.0, 1.0, 2.0, -2.0, None, False, 0.0, 1.0)
        y_1st.backward(torch.tensor([1.0]))
        grad_1st = x.grad.item()
        
        print(f"LTD 1st: {grad_1st}, 2nd: {grad_2nd}")
        self.assertTrue(abs(grad_2nd) < abs(grad_1st), "LTD 2nd order must be a brake")

if __name__ == '__main__':
    unittest.main()
