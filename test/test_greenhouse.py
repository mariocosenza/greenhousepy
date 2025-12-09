from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock

from mock import GPIO
from mock.seesaw import Seesaw
from src.greenhouse import Greenhouse, GreenhouseError


class TestGreenhouse(TestCase):

    @patch.object(Seesaw, "moisture_read")
    def test_moisture_lovel_in_range_300_500(self, moisture_sensor: Mock):
        moisture_sensor.return_value = 300
        greenhouse = Greenhouse()
        moisture_level = greenhouse.measure_soil_moisture()
        self.assertEqual(moisture_level, 300)

    @patch.object(Seesaw, "moisture_read")
    def test_moisture_lovel_outside_range_300_500_lower(self, moisture_sensor: Mock):
        moisture_sensor.return_value = 299
        greenhouse = Greenhouse()
        self.assertRaises(GreenhouseError, greenhouse.measure_soil_moisture)

    @patch.object(Seesaw, "moisture_read")
    def test_moisture_lovel_outside_range_300_500_higher(self, moisture_sensor: Mock):
        moisture_sensor.return_value = 501
        greenhouse = Greenhouse()
        self.assertRaises(GreenhouseError, greenhouse.measure_soil_moisture)

    @patch.object(GPIO, "output")
    def test_turn_on_sprinkler(self, output: Mock):
        greenhouse = Greenhouse()
        greenhouse.sprinkler_on = False
        greenhouse.turn_on_sprinkler()
        output.assert_called_once_with(greenhouse.SPRINKLER_PIN, GPIO.HIGH)
        self.assertTrue(greenhouse.sprinkler_on)

    @patch.object(GPIO, "output")
    def test_turn_off_sprinkler(self, output: Mock):
        greenhouse = Greenhouse()
        greenhouse.sprinkler_on = True
        greenhouse.turn_off_sprinkler()
        output.assert_called_once_with(greenhouse.SPRINKLER_PIN, GPIO.LOW)
        self.assertFalse(greenhouse.sprinkler_on)

    @patch.object(GPIO, "output")
    @patch.object(Seesaw, "moisture_read")
    def test_manage_sprinkler_turn_on_if_lower_than_375(self, moisture_sensor: Mock, output: Mock):
        moisture_sensor.return_value = 374
        greenhouse = Greenhouse()
        greenhouse.sprinkler_on = True
        greenhouse.manage_sprinkler()
        output.assert_called_once_with(greenhouse.SPRINKLER_PIN, GPIO.HIGH)
        self.assertTrue(greenhouse.sprinkler_on)



