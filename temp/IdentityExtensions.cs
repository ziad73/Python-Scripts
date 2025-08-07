using System.Security.Claims;

namespace CartifyBLL.Helper
{
    public static class IdentityExtensions
    {
        public static string? GetUserId(this ClaimsPrincipal user)
        {
            return user?.FindFirst(ClaimTypes.NameIdentifier)?.Value;
        }
    }
}
