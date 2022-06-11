import unittest

import usart
import time
import numpy as np

class TestCommunicationProtocol(unittest.TestCase):
    def setUp(self):
        port_name = "PORTNAME"
        self.cp = usart.CommunicationProtocol(port_name)

    def test_Control_Motor(self):
        test_patterns = [
            (2, 150, 1, 0, 0, np.array([1, 100, 0, 150, 0, 0, 0, 0, 0, 83]), 150),  # Will pass.
            (2, 0, 1, 0, 0, np.array([1, 100, 0, 0, 0, 0, 0, 0, 0, 80]), 0),  # Will pass.
            (2, -150, 1, 0, 0, np.array([1, 100, 255, 106, 0, 0, 0, 0, 0, 90]), -150),  # Will pass.
            (2, 0, 1, 0, 0, np.array([1, 100, 0, 0, 0, 0, 0, 0, 0, 80]), 0),  # Will pass.
        ]

        for Mode, Speed, ID, Acce, Brake_P, expected_Tx_result, expected_Rx_result in test_patterns:
            with self.subTest():
                self.cp.Set_MotorMode(Mode, ID)
                self.cp.Control_Motor(Speed, ID, Acce, Brake_P)
                self.assertTrue(np.allclose(self.cp._Tx, expected_Tx_result, rtol=0, atol=1))
                self.assertEqual(len(self.cp._Tx.tobytes()), 10)
                time.sleep(1)
                message = self.cp.Check_Motor()
                self.assertAlmostEqual(message[2], expected_Rx_result, delta=1)

        test_patterns = [
            (3, 0, 1, 0, 0, np.array([1, 100, 0, 0, 0, 0, 0, 0, 0, 80]), 0),  # Will pass.
            (3, 32767/4 * 1, 1, 0, 0, np.array([1, 100, 31, 255, 0, 0, 0, 0, 0, 191]), 32767/4 * 1),  # Will pass.
            (3, 32767/4 * 2, 1, 0, 0, np.array([1, 100, 63, 255, 0, 0, 0, 0, 0, 80]), 32767/4 * 2),  # Will pass.
            (3, 32767/4 * 3, 1, 0, 0, np.array([1, 100, 95, 255, 0, 0, 0, 0, 0, 120]), 32767/4 * 3),  # Will pass.
            (3, 0, 1, 0, 0, np.array([1, 100, 0, 0, 0, 0, 0, 0, 0, 80]), 0),  # Will pass.
        ]

        for Mode, Speed, ID, Acce, Brake_P, expected_Tx_result, expected_Rx_result in test_patterns:
            with self.subTest():
                self.cp.Set_MotorMode(Mode, ID)
                self.cp.Control_Motor(Speed, ID, Acce, Brake_P)
                self.assertTrue(np.allclose(self.cp._Tx, expected_Tx_result, rtol=0, atol=1))
                self.assertEqual(len(self.cp._Tx.tobytes()), 10)
                time.sleep(3)
                message = self.cp.Check_Motor()
                self.assertAlmostEqual(message[3], expected_Rx_result, delta=3)

    def test_Set_MotorMode(self):
        Mode, ID = 2, 1
        self.cp.Set_MotorMode(Mode, ID)
        self.assertEqual(len(self.cp._Tx.tobytes()), 10)
        time.sleep(1)
        message = self.cp.Get_Motor(ID)
        self.assertEqual(message[0], 2)

if __name__ == '__main__':
    unittest.main(verbosity=2)