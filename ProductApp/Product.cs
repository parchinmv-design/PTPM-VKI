namespace ProductApp
{
    public class Product
    {
        public int Id { get; set; }
        public string Arctile { get; set; }
        public string Name { get; set; }
        public decimal Price { get; set; }
        public string SupplierId { get; set; }
        public string ManufacturerId { get; set; }
        public string CategoryId { get; set; }
        public int Discount { get; set; }
        public int WarehouseCount { get; set; }
        public string Description { get; set; }
    }
}
