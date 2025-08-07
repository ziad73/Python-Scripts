using CartifyDAL.Entities.order;
using CartifyDAL.Entities.user;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CartifyBLL.ViewModels.Account
{
    public class ProfileVM
    {
        public string FullName { get; set; }
        public string Email { get; set; }
        public string PhoneNumber { get; set; }
        public string? AvatarUrl { get; set; }
        public DateTime MemberSince { get; set; }
        public int TotalOrders { get; set; }
        public int LoyaltyPoints { get; set; }
        public UserAddress DefaultShippingAddress { get; set; }
        public List<Order> RecentOrders { get; set; } = new List<Order>();
        public bool EmailVerified { get; set; }
        public bool PhoneVerified { get; set; }
        public List<AddressVM>? Addresses { get; set; }

    }
}
