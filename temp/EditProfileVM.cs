using CartifyDAL.Entities.user;
using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CartifyBLL.ViewModels.Account
{
    public class EditProfileVM
    {
        public string FullName { get; set; }
        public string PhoneNumber { get; set; }
        //public UserAddress? DefaultShippingAddress { get; set; }
        public IFormFile Avatar { get; set; }  // NEW
        public string? AvatarUrl { get; set; } // for preview display

    }
}
