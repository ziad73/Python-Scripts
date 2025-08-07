using CartifyDAL.Entities.user;
using CartifyDAL.Repo.userRepo.Abstraction;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using System.Threading.Tasks;

namespace CartifyDAL.Repo.userRepo.Impelementaion
{
    public class UserRepo : IUserRepo
    {
        private readonly UserManager<User> userManager;

        public UserRepo(UserManager<User> userManager)
        {
            this.userManager = userManager;
        }

        public async Task<User?> GetByEmailAsync(string email)
        {
            return await userManager.FindByEmailAsync(email);
        }

        public async Task<bool> AddAsync(User user, string password)
        {
            var result = await userManager.CreateAsync(user, password);
            return result.Succeeded;
        }

        public async Task<bool> RemovePasswordAsync(User user)
        {
            var result = await userManager.RemovePasswordAsync(user);
            return result.Succeeded;
        }

        public async Task<bool> AddPasswordAsync(User user, string newPassword)
        {
            var result = await userManager.AddPasswordAsync(user, newPassword);
            return result.Succeeded;
        }
        public async Task<bool> UpdateAsync(User user)
        {
            var result = await userManager.UpdateAsync(user);
            return result.Succeeded;
        }
        public async Task<User?> GetByIdAsync(string id)
        {
            return await userManager.Users.Include(u => u.Addresses).FirstOrDefaultAsync(u => u.Id == id);
        }
        public async Task<IList<string>> GetRolesAsync(User user)
        {
            return await userManager.GetRolesAsync(user);
        }
    }
}
