using CartifyBLL.ViewModels.Account;
using CartifyDAL.Entities.user;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CartifyBLL.Helper
{
    public static class UserAddressExtensions
    {
        public static AddressVM ToAddressVM(this UserAddress userAddress)
        {
            if (userAddress == null) return null;

            return new AddressVM
            {
                Id = userAddress.Id,
                Name = userAddress.Name,
                StreetAddress = userAddress.StreetAddress,
                City = userAddress.City,
                State = userAddress.State,
                PostalCode = userAddress.PostalCode,
                Country = userAddress.Country,
                PhoneNumber = userAddress.PhoneNumber,
                IsDefault = userAddress.IsDefault
            };
        }

        public static UserAddress ToUserAddress(this AddressVM addressVM)
        {
            if (addressVM == null) return null;

            return new UserAddress
            {
                Id = addressVM.Id,
                Name = addressVM.Name,
                StreetAddress = addressVM.StreetAddress,
                City = addressVM.City,
                State = addressVM.State,
                PostalCode = addressVM.PostalCode,
                Country = addressVM.Country,
                PhoneNumber = addressVM.PhoneNumber,
                IsDefault = addressVM.IsDefault
            };
        }
    }
}
