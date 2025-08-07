using CartifyBLL.Helper;
using CartifyBLL.Services.UserServices;
using CartifyBLL.ViewModels.Account;
using CartifyDAL.Entities.user;
using CartifyDAL.Repo.userRepo.Abstraction;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Identity;
using System.Net;
using System.Security.Claims;

namespace CartifyBLL.Services.UserServices
{
    public class UserService : IUserService
    {
        private readonly IUserRepo userRepo;
        private readonly UserManager<User> userManager;

        public UserService(IUserRepo userRepo, UserManager<User> userManager)
        {
            this.userRepo = userRepo;
            this.userManager = userManager;
        }

        public async Task<ProfileVM> GetUserProfileAsync(string userId)
        {
            var user = await userRepo.GetByIdAsync(userId);

            if (user == null)
                throw new Exception("User not found");

            var totalOrders = user.Orders?.Count ?? 0;
            var loyaltyPoints = totalOrders * 10;

            return new ProfileVM
            {
                FullName = user.FullName,
                Email = user.Email,
                PhoneNumber = user.PhoneNumber,
                AvatarUrl = user.AvatarUrl,
                MemberSince = user.JoinDate,
                TotalOrders = totalOrders,
                LoyaltyPoints = loyaltyPoints,
                DefaultShippingAddress = user.Addresses?.FirstOrDefault(a => a.IsDefault),
                EmailVerified = user.IsEmailVerified,
                Addresses = user.Addresses?.Select(a => a.ToAddressVM()).ToList(),
                PhoneVerified = !string.IsNullOrEmpty(user.PhoneNumber)
            };
        }

        public async Task<IdentityResult> UpdateUserProfileAsync(string userId, EditProfileVM model)
        {
            var user = await userRepo.GetByIdAsync(userId);
            if (user == null)
                return IdentityResult.Failed(new IdentityError { Description = "User not found" });

            user.FullName = model.FullName;
            user.PhoneNumber = model.PhoneNumber;

            if (model.Avatar != null && model.Avatar.Length > 0)
            {
                if (!string.IsNullOrEmpty(user.AvatarUrl))
                {
                    var oldFile = Path.GetFileName(user.AvatarUrl);
                    FileUploader.RemoveFile("Avatars", oldFile);
                }

                var avatarPath = FileUploader.UploadFile("Avatars", model.Avatar);
                if (!string.IsNullOrEmpty(avatarPath))
                {
                    user.AvatarUrl = avatarPath;
                }
            }

            return await userManager.UpdateAsync(user);
        }

        public async Task<IdentityResult> ChangePasswordAsync(string userId, string oldPassword, string newPassword)
        {
            var user = await userRepo.GetByIdAsync(userId);
            if (user == null)
                return IdentityResult.Failed(new IdentityError { Description = "User not found" });

            return await userManager.ChangePasswordAsync(user, oldPassword, newPassword);
        }

        public async Task<(bool Succeeded, string AvatarUrl, IEnumerable<string> Errors)> UploadAvatarAsync(string userId, IFormFile avatar)
        {
            var user = await userRepo.GetByIdAsync(userId);
            if (user == null)
                return (false, "", new[] { "User not found" });

            // Remove previous avatar if exists
            if (!string.IsNullOrEmpty(user.AvatarUrl))
            {
                string oldFileName = Path.GetFileName(user.AvatarUrl); // extract "abc.jpg" from "/Files/Avatars/abc.jpg"
                FileUploader.RemoveFile("Avatars", oldFileName);
            }

            // Upload new avatar using helper
            var newAvatarPath = FileUploader.UploadFile("Avatars", avatar);
            if (string.IsNullOrEmpty(newAvatarPath))
                return (false, "", new[] { "Failed to upload avatar." });

            user.AvatarUrl = newAvatarPath;

            var result = await userManager.UpdateAsync(user);
            return (result.Succeeded, user.AvatarUrl, result.Errors.Select(e => e.Description));
        }

        public async Task<IdentityResult> AddAddressAsync(string userId, AddressVM model)
        {
            var user = await userRepo.GetByIdAsync(userId);
            if (user == null)
                return IdentityResult.Failed(new IdentityError { Description = "User not found" });

            var address = new UserAddress
            {
                StreetAddress = model.StreetAddress,
                City = model.City,
                State = model.State,
                PostalCode = model.PostalCode,
                Country = model.Country,
                PhoneNumber = model.PhoneNumber,
                IsDefault = model.IsDefault,
                Name = model.Name
            };

            if (user.Addresses == null)
            {
                user.Addresses = new List<UserAddress>();
            }

            // If this is the first address or marked as default, set as default
            if (model.IsDefault || !user.Addresses.Any())
            {
                foreach (var existingAddress in user.Addresses)
                {
                    existingAddress.IsDefault = false;
                }
                address.IsDefault = true;
            }

            user.Addresses.Add(address);
            return await userManager.UpdateAsync(user);
        }

        public async Task<IdentityResult> UpdateAddressAsync(string userId, AddressVM model)
        {
            var user = await userRepo.GetByIdAsync(userId);
            if (user == null)
                return IdentityResult.Failed(new IdentityError { Description = "User not found" });

            var address = user.Addresses?.FirstOrDefault(a => a.Id == model.Id);
            if (address == null)
                return IdentityResult.Failed(new IdentityError { Description = "Address not found" });

            address.StreetAddress = model.StreetAddress;
            address.City = model.City;
            address.State = model.State;
            address.PostalCode = model.PostalCode;
            address.Country = model.Country;
            address.PhoneNumber = model.PhoneNumber;
            address.Name = model.Name;

            // Always reset default for all addresses
            foreach (var existingAddress in user.Addresses)
            {
                existingAddress.IsDefault = false;
            }

            // Then set this one as default if requested
            address.IsDefault = model.IsDefault;

            return await userManager.UpdateAsync(user);
        }

        public async Task<IdentityResult> DeleteAddressAsync(string userId, int addressId)
        {
            var user = await userRepo.GetByIdAsync(userId);
            if (user == null)
                return IdentityResult.Failed(new IdentityError { Description = "User not found" });

            var address = user.Addresses?.FirstOrDefault(a => a.Id == addressId);
            if (address == null)
                return IdentityResult.Failed(new IdentityError { Description = "Address not found" });

            user.Addresses.Remove(address);
            return await userManager.UpdateAsync(user);
        }

        public async Task<IdentityResult> SetDefaultAddressAsync(string userId, int addressId)
        {
            var user = await userRepo.GetByIdAsync(userId);
            if (user == null)
                return IdentityResult.Failed(new IdentityError { Description = "User not found" });

            var address = user.Addresses?.FirstOrDefault(a => a.Id == addressId);
            if (address == null)
                return IdentityResult.Failed(new IdentityError { Description = "Address not found" });

            // Reset all other addresses to non-default
            foreach (var addr in user.Addresses)
            {
                addr.IsDefault = false;
            }

            // Set the selected address as default
            address.IsDefault = true;

            return await userManager.UpdateAsync(user);
        }
        public async Task<AddressVM> GetAddressAsync(string userId, int addressId)
        {
            var user = await userRepo.GetByIdAsync(userId);
            if (user == null)
                throw new Exception("User not found");

            var address = user.Addresses?.FirstOrDefault(a => a.Id == addressId);
            if (address == null)
                throw new Exception("Address not found");

            return new AddressVM
            {
                Id = address.Id,
                Name = address.Name,
                StreetAddress = address.StreetAddress,
                City = address.City,
                State = address.State,
                PostalCode = address.PostalCode,
                Country = address.Country,
                PhoneNumber = address.PhoneNumber,
                IsDefault = address.IsDefault
            };
        }




    }
}
