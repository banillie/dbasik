import pathlib
import unittest
from datetime import date

from dbasik.datamap.models import DatamapLine
from dbasik.excelparser.helpers.parser import (
    CellData,
    CellValueType,
    ParsedSpreadsheet,
    _filter_phone_ints,
)
from dbasik.factories.datamap_factories import DatamapFactory, ProjectFactory
from dbasik.register.models import FinancialQuarter
from dbasik.returns.models import Return, ReturnItem
from django.test import TestCase


class TestErroneousFigure(TestCase):
    """Figures in the template in form of 1m should not be parsed as dates."""

    def setUp(self):
        self.financial_quarter = FinancialQuarter.objects.create(quarter=4, year=2018)
        self.project = ProjectFactory()
        self.datamap = DatamapFactory()
        self.return_obj = Return.objects.create(
            project=self.project, financial_quarter=self.financial_quarter
        )
        # This is a sanity check to test that the int 1_000_000 with no formatting works
        DatamapLine.objects.create(
            datamap=self.datamap,
            key="PoC email",
            sheet="rpt_template",
            cell_ref="E59",
        )
        DatamapLine.objects.create(
            datamap=self.datamap,
            key="Total Costs Spent",
            sheet="rpt_template",
            cell_ref="E111",
        )
        DatamapLine.objects.create(
            datamap=self.datamap,
            key="Total Costs Remaining",
            sheet="rpt_template",
            cell_ref="E112",
        )

        self.populated_template = (
            pathlib.Path(__file__).parent.absolute()
            / "project_sheet_with_1m_numbers.xlsm"
        )
        self.parsed_spreadsheet = ParsedSpreadsheet(
            template_path=self.populated_template,
            project=self.project,
            return_obj=self.return_obj,
            datamap=self.datamap,
        )

    def test_return_1m_ok(self):
        """testing 1_000_000 is fine."""
        self.parsed_spreadsheet.process()
        return_items = (
            Return.objects.get(id=self.return_obj.id)
            .return_returnitems.all()
            .order_by("datamapline_id")
        )
        poc_r = return_items[0]
        self.assertEqual(poc_r.datamapline.key, "PoC email")
        self.assertEqual(poc_r.value_int, 1_000_000)
        self.assertEqual(poc_r.value_date, None)

    @unittest.skip("TODO - FAILS FOR SOME UNKNOWN REASON")
    def test_return_parser(self):
        """testing use of '\£#\m' format code, which needs to be parsed correctly"""
        self.parsed_spreadsheet.process()
        return_items = Return.objects.get(
            id=self.return_obj.id
        ).return_returnitems.all()
        total_line = return_items[1]
        self.assertEqual(total_line.datamapline.key, "Total Costs Spent")
        self.assertEqual(total_line.value_int, 1_000_000)
        self.assertEqual(total_line.value_date, None)


class TestParseToReturn(TestCase):
    def setUp(self):
        self.financial_quarter = FinancialQuarter.objects.create(quarter=4, year=2018)
        self.project = ProjectFactory()
        self.datamap = DatamapFactory()
        self.return_obj = Return.objects.create(
            project=self.project, financial_quarter=self.financial_quarter
        )
        DatamapLine.objects.create(
            datamap=self.datamap,
            key="Project Name",
            sheet="Test Sheet 1",
            cell_ref="B1",
        )
        DatamapLine.objects.create(
            datamap=self.datamap, key="Total Cost", sheet="Test Sheet 1", cell_ref="B2"
        )
        DatamapLine.objects.create(
            datamap=self.datamap, key="SRO", sheet="Test Sheet 1", cell_ref="B3"
        )
        DatamapLine.objects.create(
            datamap=self.datamap,
            key="SRO Retirement Date",
            sheet="Test Sheet 1",
            cell_ref="B4",
        )
        DatamapLine.objects.create(
            datamap=self.datamap,
            key="Missing Data",
            sheet="Test Sheet 1",
            cell_ref="B5",
        )
        DatamapLine.objects.create(
            datamap=self.datamap,
            key="Janitor's Favourite Colour",
            sheet="Test Sheet 2",
            cell_ref="B1",
        )
        DatamapLine.objects.create(
            datamap=self.datamap,
            key="Corkys Phone",
            sheet="Test Sheet 1",
            cell_ref="B6",
            data_type="Phone",
        )

        self.populated_template = (
            pathlib.Path(__file__).parent.absolute() / "populated.xlsm"
        )
        self.parsed_spreadsheet = ParsedSpreadsheet(
            template_path=self.populated_template,
            project=self.project,
            return_obj=self.return_obj,
            datamap=self.datamap,
        )

    def test_convert_phone_ints_to_str(self):
        d = CellData("nothing", "no sheet", 7823232231, "A1", CellValueType.PHONE)
        out = _filter_phone_ints(d)
        self.assertEqual(
            out,
            CellData("nothing", "no sheet", "7823232231", "A1", CellValueType.PHONE),
        )

    def test_convert_phone_ints_to_str_passthru(self):
        d = CellData("nothing", "no sheet", 7823232231, "A1", CellValueType.INTEGER)
        d2 = CellData("nothing", "no sheet", "7823232231", "A1", CellValueType.STRING)
        out = _filter_phone_ints(d)
        out2 = _filter_phone_ints(d2)
        self.assertEqual(
            out,
            CellData("nothing", "no sheet", 7823232231, "A1", CellValueType.INTEGER),
        )
        self.assertEqual(
            out2,
            CellData("nothing", "no sheet", "7823232231", "A1", CellValueType.STRING),
        )

    def test_return_parser(self):
        self.parsed_spreadsheet.process()
        return_item = Return.objects.get(
            id=self.return_obj.id
        ).return_returnitems.first()
        self.assertEqual(return_item.datamapline.key, "Project Name")
        self.assertEqual(return_item.value_str, "Testable Project")

    def test_phone_number_is_handled_as_str(self):
        self.parsed_spreadsheet.process()
        dml = DatamapLine.objects.filter(key="Corkys Phone")
        return_item = ReturnItem.objects.filter(datamapline_id=dml.first().id).first()
        self.assertEqual(return_item.value_phone, "7844695632")

    def test_celldata_mapper(self):
        self.parsed_spreadsheet.process()
        cell_data_int = CellData("Key", "Sheet", 1, "B1", CellValueType.INTEGER)
        cell_data_float = CellData("Key", "Sheet", 1, "B1", CellValueType.FLOAT)
        cell_data_date = CellData(
            "Key", "Sheet", date(2018, 1, 1), "B1", CellValueType.DATE
        )
        self.assertEqual(
            self.parsed_spreadsheet._map_to_keyword_param(cell_data_int), "value_int"
        )
        self.assertEqual(
            self.parsed_spreadsheet._map_to_keyword_param(cell_data_float),
            "value_float",
        )
        self.assertEqual(
            self.parsed_spreadsheet._map_to_keyword_param(cell_data_date), "value_date"
        )

    def test_parse_to_return_object(self):
        self.parsed_spreadsheet.process()

        dml_project_name = (
            DatamapLine.objects.filter(datamap=self.datamap)
            .filter(key="Project Name")
            .first()
        )
        dml_sro_retirement = (
            DatamapLine.objects.filter(datamap=self.datamap)
            .filter(key="SRO Retirement Date")
            .first()
        )
        dml_sro = (
            DatamapLine.objects.filter(datamap=self.datamap).filter(key="SRO").first()
        )

        dml_missing_data = (
            DatamapLine.objects.filter(datamap=self.datamap)
            .filter(key="Missing Data")
            .first()
        )

        return_item_projectname = (
            Return.objects.get(id=self.return_obj.id)
            .return_returnitems.filter(datamapline=dml_project_name)
            .first()
        )
        return_item_srocell = (
            Return.objects.get(id=self.return_obj.id)
            .return_returnitems.filter(datamapline=dml_sro_retirement)
            .first()
        )
        return_item_sro = (
            Return.objects.get(id=self.return_obj.id)
            .return_returnitems.filter(datamapline=dml_sro)
            .first()
        )
        return_item_missing_data = (
            Return.objects.get(id=self.return_obj.id)
            .return_returnitems.filter(datamapline=dml_missing_data)
            .first()
        )

        self.assertEqual(return_item_projectname.datamapline.key, "Project Name")
        self.assertEqual(return_item_projectname.value_str, "Testable Project")

        self.assertEqual(return_item_srocell.datamapline.key, "SRO Retirement Date")
        self.assertEqual(return_item_srocell.value_date, date(2022, 2, 23))

        self.assertEqual(return_item_sro.datamapline.key, "SRO")
        self.assertEqual(return_item_sro.value_str, "John Milton")
        self.assertEqual(return_item_sro.value_int, None)
        self.assertEqual(return_item_sro.value_date, None)

        self.assertEqual(return_item_missing_data.datamapline.key, "Missing Data")
        self.assertIsNone(return_item_missing_data.value_date)
        self.assertIsNone(return_item_missing_data.value_str)
        self.assertIsNone(return_item_missing_data.value_float)
