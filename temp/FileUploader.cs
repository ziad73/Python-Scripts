using Microsoft.AspNetCore.Http;

namespace CartifyBLL.Helper
{
    public static class FileUploader
    {
        public static string UploadFile(string folderName, IFormFile file)
        {
            try
            {
                string folderPath = Path.Combine(Directory.GetCurrentDirectory(), "wwwroot", "Files", folderName);
                Directory.CreateDirectory(folderPath);

                string fileName = Guid.NewGuid() + Path.GetExtension(file.FileName);
                string finalPath = Path.Combine(folderPath, fileName);

                using (var stream = new FileStream(finalPath, FileMode.Create))
                {
                    file.CopyTo(stream);
                }

                return $"/Files/{folderName}/{fileName}";
            }
            catch
            {
                return null;
            }
        }

        public static string RemoveFile(string folderName, string fileName)
        {
            try
            {
                var path = Path.Combine(Directory.GetCurrentDirectory(), "wwwroot", "Files", folderName, fileName);
                if (System.IO.File.Exists(path))
                {
                    System.IO.File.Delete(path);
                    return "Deleted";
                }

                return "File not found";
            }
            catch (Exception ex)
            {
                return ex.Message;
            }
        }
    }
}
