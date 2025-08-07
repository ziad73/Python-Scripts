using CartifyBLL.Helper;
using CartifyBLL.Services.UserServices;
using CartifyBLL.ViewModels.Account;
using CartifyDAL.Entities.user;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.ModelBinding;
using System.Security.Claims;

namespace CartifyPLL.Controllers
{
    public class AccountController : Controller
    {
        private readonly IAccountService accountService;
        private readonly SignInManager<User> signInManager;
        private readonly UserManager<User> userManager;
        private readonly IUserService _userService;
        //private readonly IOrderService orderService;


        public AccountController(
    IAccountService accountService,
    SignInManager<User> signInManager,
    UserManager<User> userManager, IUserService _userService)//, IOrderService _orderService)
        {
            this.accountService = accountService;
            this.signInManager = signInManager;
            this.userManager = userManager;
            this._userService = _userService;
            //this.orderService = _orderService;

        }

        [HttpGet]
        public IActionResult Login()
        {
            return View("LoginView");
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Login(LoginVM model)
        {
            if (!ModelState.IsValid)
                return View("LoginView", model);

            var (success, error, isEmailNotConfirmed) = await accountService.LoginAsync(model);

            if (isEmailNotConfirmed)
            {
                TempData["Email"] = model.Email;
                TempData["VerificationPurpose"] = "Register"; // Or "Reset" if this is from forgot password

                return View("EmailCodeVerificationView", new EmailCodeVM
                {
                    Email = model.Email,
                    Purpose = "Register"
                });
            }

            if (success)
            {
                var user = await userManager.FindByEmailAsync(model.Email);
                if (user != null && await userManager.IsInRoleAsync(user, "Admin"))
                {
                    return RedirectToAction("Index", "AdminDashboard", new { area = "Admin" });
                }

                return RedirectToAction("Index", "Home");

            }


            ModelState.AddModelError("", error);
            return View("LoginView", model);
        }


        [HttpGet]
        public IActionResult Register()
        {
            return View("RegisterView");
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Register(RegisterVM model)
        {
            if (!ModelState.IsValid)
                return View("RegisterView", model);

            var (success, error) = await accountService.RegisterAsync(model);
            if (success)
            {
                TempData["Email"] = model.Email;
                TempData["VerificationPurpose"] = "Register";

                return View("EmailCodeVerificationView", new EmailCodeVM
                {
                    Email = model.Email,
                    Purpose = "Register"
                });
            }

            ModelState.AddModelError("", error);
            return View("RegisterView", model);
        }

        [HttpGet]
        public IActionResult VerifyEmail()
        {
            return View("VerifyEmailView");
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> VerifyEmail(VerifyEmailVM model)
        {
            if (!ModelState.IsValid)
                return View("VerifyEmailView", model);

            TempData["Email"] = model.Email;
            TempData["VerificationPurpose"] = "Reset";

            var sent = await accountService.SendVerificationCodeAsync(model.Email, "Reset");
            if (!sent)
            {
                ModelState.AddModelError("", "Failed to send verification code. Please check the email.");
                return View("VerifyEmailView", model);
            }

            return View("EmailCodeVerificationView", new EmailCodeVM
            {
                Email = model.Email,
                Purpose = "Reset"
            });
        }

        [HttpGet]
        public IActionResult ResetPassword(string email)
        {
            if (string.IsNullOrEmpty(email))
                return RedirectToAction("VerifyEmail");

            return View("ResetPasswordView", new ResetPasswordVM { Email = email });
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> ResetPassword(ResetPasswordVM model)
        {
            if (!ModelState.IsValid)
                return View("ResetPasswordView", model);

            var (success, error) = await accountService.ResetPasswordAsync(model);
            if (success)
                return RedirectToAction("Login");

            ModelState.AddModelError("", error);
            return View("ResetPasswordView", model);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> EmailCodeVerification(EmailCodeVM model)
        {
            if (!ModelState.IsValid)
                return View("EmailCodeVerificationView", model);

            var result = await accountService.ConfirmEmailCodeAsync(model);

            if (!result.Success)
            {
                ModelState.AddModelError("", result.ErrorMessage);
                return View("EmailCodeVerificationView", model);
            }

            if (model.Purpose == "Reset")
                return RedirectToAction("ResetPassword", new { email = model.Email });

            return RedirectToAction("Login");
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Logout()
        {
            await HttpContext.SignOutAsync(IdentityConstants.ApplicationScheme);
            return RedirectToAction("Index", "Home");
        }

        [HttpPost]
        [AllowAnonymous]
        [ValidateAntiForgeryToken]
        public IActionResult ExternalLogin(string provider, string? returnUrl = null)
        {
            var redirectUrl = Url.Action("ExternalLoginCallback", "Account", new { ReturnUrl = returnUrl });
            var properties = signInManager.ConfigureExternalAuthenticationProperties(provider, redirectUrl);
            return Challenge(properties, provider);
        }
        [AllowAnonymous]
        public async Task<IActionResult> ExternalLoginCallback(string? returnUrl = null, string? remoteError = null)
        {
            returnUrl ??= Url.Content("~/");

            if (remoteError != null)
            {
                ModelState.AddModelError(string.Empty, $"Error from external provider: {remoteError}");
                return View("LoginView");
            }

            var info = await signInManager.GetExternalLoginInfoAsync();
            if (info == null)
                return RedirectToAction(nameof(Login));

            // Try to log in the user with external login info
            var result = await signInManager.ExternalLoginSignInAsync(
                info.LoginProvider,
                info.ProviderKey,
                isPersistent: false,
                bypassTwoFactor: true);

            if (result.Succeeded)
            {
                return LocalRedirect(returnUrl);
            }

            // Try to get email from external provider
            var email = info.Principal.FindFirstValue(ClaimTypes.Email);
            var name = info.Principal.FindFirstValue(ClaimTypes.Name) ?? email;

            if (email == null)
            {
                ModelState.AddModelError(string.Empty, "Email not received from external provider.");
                return View("LoginView");
            }

            // Check if user already exists by email
            var existingUser = await userManager.FindByEmailAsync(email);

            if (existingUser != null)
            {
                // Link the external login and sign in
                await userManager.AddLoginAsync(existingUser, info);
                await signInManager.SignInAsync(existingUser, isPersistent: false);
                return LocalRedirect(returnUrl);
            }

            // User does not exist, create a new one
            var newUser = new User
            {
                UserName = email,
                Email = email,
                FullName = name
            };

            var createResult = await userManager.CreateAsync(newUser);
            if (createResult.Succeeded)
            {
                await userManager.AddLoginAsync(newUser, info);
                await signInManager.SignInAsync(newUser, isPersistent: false);
                return LocalRedirect(returnUrl);
            }

            foreach (var error in createResult.Errors)
                ModelState.AddModelError(string.Empty, error.Description);

            return View("LoginView");
        }


        [HttpGet]
        public async Task<ActionResult> Profile()
        {
            var userId = User.GetUserId();
            var userProfile = await _userService.GetUserProfileAsync(userId);
            //var recentOrders = await _orderService.GetRecentOrdersAsync(userId, 3);

            var model = new ProfileVM
            {
                FullName = userProfile.FullName,
                Email = userProfile.Email,
                PhoneNumber = userProfile.PhoneNumber,
                MemberSince = userProfile.MemberSince,
                TotalOrders = userProfile.TotalOrders,
                LoyaltyPoints = userProfile.LoyaltyPoints,
                Addresses = userProfile.Addresses, 
                DefaultShippingAddress = userProfile.DefaultShippingAddress,
                //RecentOrders = recentOrders,
                EmailVerified = userProfile.EmailVerified,
                PhoneVerified = userProfile.PhoneVerified,
                AvatarUrl = userProfile.AvatarUrl
            };

            return View("ProfileView",model);
        }


        [HttpGet]
        public async Task<ActionResult> EditProfile()
        {
            var userId = User.GetUserId();
            var userProfile = await _userService.GetUserProfileAsync(userId);
            var model = new EditProfileVM
            {
                FullName = userProfile.FullName,
                PhoneNumber = userProfile.PhoneNumber,
                //DefaultShippingAddress = userProfile.DefaultShippingAddress
                AvatarUrl=userProfile.AvatarUrl
            };

            return View("EditProfileView", model);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<ActionResult> EditProfile(EditProfileVM model)
        {
            if (!ModelState.IsValid)
                return View(model);

            var userId = User.GetUserId();
            var result = await _userService.UpdateUserProfileAsync(userId, model);

            if (result.Succeeded)
            {
                TempData["SuccessMessage"] = "Your profile has been updated successfully.";
                return RedirectToAction("Profile");
            }

            foreach (var error in result.Errors)
            {
                ModelState.AddModelError("", error.Description);
            }

            return View("EditProfileView",model);
        }


        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<ActionResult> UploadAvatar(IFormFile avatar)
        {
            if (avatar == null || avatar.Length == 0)
            {
                return Json(new { success = false, message = "No file uploaded." });
            }

            if (!avatar.ContentType.StartsWith("image/"))
            {
                return Json(new { success = false, message = "Only image files are allowed." });
            }

            if (avatar.Length > 5 * 1024 * 1024) // 5MB
            {
                return Json(new { success = false, message = "File size must be less than 5MB." });
            }

            try
            {
                var userId = User.GetUserId();
                var result = await _userService.UploadAvatarAsync(userId, avatar);

                if (result.Succeeded)
                {
                    return Json(new
                    {
                        success = true,
                        avatarUrl = result.AvatarUrl
                    });
                }

                return Json(new
                {
                    success = false,
                    message = string.Join(" ", result.Errors)
                });
            }
            catch (Exception)
            {
                return Json(new
                {
                    success = false,
                    message = "An error occurred while uploading your avatar."
                });
            }
        }


        [HttpGet]
        public async Task<IActionResult> AddAddress()
        {
            return View(new AddressVM());
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> AddAddress(AddressVM model)
        {
            if (!ModelState.IsValid)
                return View(model);

            var userId = User.GetUserId();
            var result = await _userService.AddAddressAsync(userId, model);

            if (result.Succeeded)
            {
                TempData["SuccessMessage"] = "Address added successfully";
                return RedirectToAction("Profile");
            }

            foreach (var error in result.Errors)
            {
                ModelState.AddModelError("", error.Description);
            }

            return View(model);
        }

        [HttpGet]
        public async Task<IActionResult> EditAddress(int id)
        {
            var userId = User.GetUserId();
            var address = await _userService.GetAddressAsync(userId, id);

            if (address == null)
                return NotFound();

            return View(address);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> EditAddress(AddressVM model)
        {
            if (!ModelState.IsValid)
                return View(model);

            var userId = User.GetUserId();
            var result = await _userService.UpdateAddressAsync(userId, model);

            if (result.Succeeded)
            {
                TempData["SuccessMessage"] = "Address updated successfully";
                return RedirectToAction("Profile");
            }

            foreach (var error in result.Errors)
            {
                ModelState.AddModelError("", error.Description);
            }

            return View(model);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> SetDefaultAddress([FromBody] SetDefaultAddressRequest request)
        {
            try
            {
                var userId = User.GetUserId();
                var result = await _userService.SetDefaultAddressAsync(userId, request.id);

                if (!result.Succeeded)
                {
                    return Json(new
                    {
                        success = false,
                        message = result.Errors.FirstOrDefault()?.Description ?? "Failed to set default address"
                    });
                }

                return Json(new { success = true });
            }
            catch (Exception ex)
            {
                return Json(new
                {
                    success = false,
                    message = "An error occurred: " + ex.Message
                });
            }
        }

        public class SetDefaultAddressRequest
        {
            public int id { get; set; }
        }
        [HttpPost]
        public async Task<IActionResult> DeleteAddress(int id)
        {
            var userId = User.GetUserId();
            var result = await _userService.DeleteAddressAsync(userId, id);

            return RedirectToAction("Profile");
        }

    }
}

