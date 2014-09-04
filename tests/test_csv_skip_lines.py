import six
if six.PY3:
    from io import StringIO
else:
    from StringIO import StringIO

from .config import COLUMNS_1, IPHONE_DATA, IPAD_DATA, VALID_TEMPLATE_STR
from .base import BaseSmartCSVTestCase

import smartcsv
from smartcsv.exceptions import InvalidCSVException


class CSVSkipFirstNLinesTestCase(BaseSmartCSVTestCase):
    def test_valid_data_without_specifying_a_header(self):
        """Should be valid and parse data ok if no header is provided in the CSV"""
        csv_data = """
{iphone_data}
{ipad_data}
        """.format(
            iphone_data=VALID_TEMPLATE_STR.format(**IPHONE_DATA),
            ipad_data=VALID_TEMPLATE_STR.format(**IPAD_DATA),
        )
        reader = smartcsv.reader(
            StringIO(csv_data), columns=COLUMNS_1, header_included=False)

        iphone = next(reader)
        ipad = next(reader)

        self.assertRaises(StopIteration, lambda: list(next(reader)))

        self.assertTrue(
            isinstance(iphone, dict) and isinstance(ipad, dict))

        self.assertModelsEquals(iphone, IPHONE_DATA)
        self.assertModelsEquals(ipad, IPAD_DATA)

    def test_invalid_data_without_specifiying_a_header(self):
        """Should fail if the data is invalid and no header was provided."""
        # Missing category field
        csv_data = """
iPhone 5c blue,Smartphones,USD,699,http://apple.com/iphone,http://apple.com/iphone.jpg
        """
        reader = smartcsv.reader(
            StringIO(csv_data), columns=COLUMNS_1, header_included=False)

        try:
            next(reader)
        except InvalidCSVException as e:
            self.assertTrue(e.errors is not None)
            self.assertTrue('row_length' in e.errors)
        else:
            assert False, "Shouldn't pass. Exception expected."

    def test_valid_data_and_skip_lines_without_header(self):
        """Should skip the first N lines and parse data ok without a header"""
        csv_data = """
Generated by Autobot 2000 - V0.1.2
----------
This next is intentionally left blank

-- Beginning of content
{iphone_data}
{ipad_data}
        """.format(
            iphone_data=VALID_TEMPLATE_STR.format(**IPHONE_DATA),
            ipad_data=VALID_TEMPLATE_STR.format(**IPAD_DATA),
        )
        reader = smartcsv.reader(
            StringIO(csv_data), columns=COLUMNS_1, header_included=False,
            skip_lines=6)

        iphone = next(reader)
        ipad = next(reader)

        self.assertRaises(StopIteration, lambda: list(next(reader)))

        self.assertTrue(
            isinstance(iphone, dict) and isinstance(ipad, dict))

        self.assertModelsEquals(iphone, IPHONE_DATA)
        self.assertModelsEquals(ipad, IPAD_DATA)

    def test_valid_data_and_skip_lines_with_header(self):
        """Should skip the first N lines and parse data ok with header"""
        csv_data = """
Generated by Autobot 2000 - V0.1.2
----------
This next is intentionally left blank

-- Beginning of content
title,category,subcategory,currency,price,url,image_url
{iphone_data}
{ipad_data}
        """.format(
            iphone_data=VALID_TEMPLATE_STR.format(**IPHONE_DATA),
            ipad_data=VALID_TEMPLATE_STR.format(**IPAD_DATA),
        )
        reader = smartcsv.reader(
            StringIO(csv_data), columns=COLUMNS_1, skip_lines=6)

        iphone = next(reader)
        ipad = next(reader)

        self.assertRaises(StopIteration, lambda: list(next(reader)))

        self.assertTrue(
            isinstance(iphone, dict) and isinstance(ipad, dict))

        self.assertModelsEquals(iphone, IPHONE_DATA)
        self.assertModelsEquals(ipad, IPAD_DATA)

    def test_skip_lines_with_invalid_value(self):
        """Should raise an exception if an invalid value for skip lines is given"""
        csv_data = """
        Generated by Autobot 2000 - V0.1.2
        ----------
        This next is intentionally left blank

        -- Beginning of content
{iphone_data}
{ipad_data}
         """.format(
            iphone_data=VALID_TEMPLATE_STR.format(**IPHONE_DATA),
            ipad_data=VALID_TEMPLATE_STR.format(**IPAD_DATA),
        )

        def _create_reader():
            reader = smartcsv.reader(
                StringIO(csv_data), columns=COLUMNS_1, skip_lines=10)

        self.assertRaises(AttributeError, _create_reader)
