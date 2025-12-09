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

