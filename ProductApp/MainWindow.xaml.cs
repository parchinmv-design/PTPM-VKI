using ClosedXML.Excel;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;

namespace ProductApp
{
    public partial class MainWindow : Window
    {
        private List<Product> _products = new();

        public MainWindow()
        {
            InitializeComponent();
            LoadData();
        }

        private void LoadData()
        {
            var wb = new XLWorkbook("Product.xlsx");
            var ws = wb.Worksheet(1);
            _products = ws.RangeUsed().RowsUsed().Skip(1).Select(r => new Product
            {
                Id = r.Cell(1).GetValue<int>(),
                Arctile = r.Cell(2).GetString(),
                Name = r.Cell(3).GetString(),
                Price = r.Cell(4).GetValue<decimal>(),
                SupplierId = r.Cell(5).GetString(),
                ManufacturerId = r.Cell(6).GetString(),
                CategoryId = r.Cell(7).GetString(),
                Discount = r.Cell(8).GetValue<int>(),
                WarehouseCount = r.Cell(9).GetValue<int>(),
                Description = r.Cell(10).GetString()
            }).ToList();

            ManufacturerFilter.ItemsSource = _products.Select(p => p.ManufacturerId).Distinct().OrderBy(m => m).ToList();
            SupplierFilter.ItemsSource = _products.Select(p => p.SupplierId).Distinct().OrderBy(s => s).ToList();

            ApplyFilters();
        }

        private void Filter_Changed(object sender, SelectionChangedEventArgs e) => ApplyFilters();
        private void SortFilter_Changed(object sender, SelectionChangedEventArgs e) => ApplyFilters();

        private void ResetButton_Click(object sender, RoutedEventArgs e)
        {
            ManufacturerFilter.SelectedItem = null;
            SupplierFilter.SelectedItem = null;
            SortFilter.SelectedItem = null;
            ApplyFilters();
        }

        private void ApplyFilters()
        {
            var view = CollectionViewSource.GetDefaultView(_products);

            view.Filter = item =>
            {
                var p = (Product)item;
                var mOk = ManufacturerFilter.SelectedItem == null || p.ManufacturerId == (string)ManufacturerFilter.SelectedItem;
                var sOk = SupplierFilter.SelectedItem == null || p.SupplierId == (string)SupplierFilter.SelectedItem;
                return mOk && sOk;
            };

            view.SortDescriptions.Clear();
            if (SortFilter?.SelectedIndex == 1)
                view.SortDescriptions.Add(new SortDescription("Discount", ListSortDirection.Descending));
            else if (SortFilter?.SelectedIndex == 2)
                view.SortDescriptions.Add(new SortDescription("Discount", ListSortDirection.Ascending));

            ProductsList.ItemsSource = view;
            CountLabel.Text = $"Найдено товаров: {view.Cast<object>().Count()}";
        }
    }
}
