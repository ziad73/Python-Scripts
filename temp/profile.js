document.addEventListener("DOMContentLoaded", function () {
    // Initialize tab functionality
    $('#profileTabs a').on('click', function (e) {
        e.preventDefault();
        $(this).tab('show');

        // Store the active tab in localStorage
        localStorage.setItem('activeProfileTab', $(this).attr('href'));
    });

    // Retrieve active tab from localStorage
    var activeTab = localStorage.getItem('activeProfileTab');
    if (activeTab) {
        $('#profileTabs a[href="' + activeTab + '"]').tab('show');
    }

    // Avatar upload preview
    document.getElementById('avatarUpload')?.addEventListener('change', function (e) {
        if (this.files && this.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                document.getElementById('profileAvatar').src = e.target.result;
                uploadAvatar(this.files[0]);
            }

            reader.readAsDataURL(this.files[0]);
        }
    });

    // Initialize tooltips
    $('[data-toggle="tooltip"]').tooltip();
});

function uploadAvatar(file) {
    var formData = new FormData();
    formData.append('avatar', file);

    $.ajax({
        url: '/Account/UploadAvatar',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        headers: {
            'RequestVerificationToken': $('input[name="__RequestVerificationToken"]').val()
                || $('meta[name="csrf-token"]').attr('content')
        },
        success: function (response) {
            if (response.success) {
                document.getElementById('profileAvatar').src = response.avatarUrl;
                showToast('Avatar updated successfully!', 'success');
            } else {
                showToast('Error updating avatar: ' + response.message, 'error');
            }
        },
        error: function (xhr, status, error) {
            showToast('Error uploading avatar: ' + error, 'error');
        }
    });
}


function showToast(message, type) {
    // Implement toast notification or use a library like Toastr
    console.log(`${type}: ${message}`);
    // Example with Toastr:
    // toastr[type](message);
}

function getStatusBadgeClass(status) {
    switch (status.toLowerCase()) {
        case 'delivered': return 'badge-success';
        case 'shipped': return 'badge-info';
        case 'processing': return 'badge-primary';
        case 'pending': return 'badge-warning';
        case 'cancelled': return 'badge-danger';
        default: return 'badge-secondary';
    }
}

// Avatar upload functionality
document.getElementById('avatarUpload').addEventListener('change', function (e) {
    if (this.files && this.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            document.getElementById('profileAvatar').src = e.target.result;

            // Here you would typically upload the image to the server
            // using AJAX or submit a form
        }

        reader.readAsDataURL(this.files[0]);
    }
});
// Handle sidebar tab links
document.querySelectorAll('.list-group-item a[href^="#"]').forEach(link => {
    link.addEventListener('click', function (e) {
        e.preventDefault();
        const tabId = this.getAttribute('href');
        $(tabId).tab('show');
        localStorage.setItem('activeProfileTab', tabId);
    });
});
@if (Model.Addresses != null && Model.Addresses.Any()) {
    foreach(var address in Model.Addresses)
    {
        @if (address.IsDefault) {
            @await Html.PartialAsync("_DeleteAddressModal", address)
        }
    }
}
// Delete address confirmation
$(document).ready(function () {
    $('.delete-address-btn').click(function (e) {
        e.preventDefault();
        var addressId = $(this).data('address-id');
        $('#deleteAddressModal').modal('show');
        $('#deleteAddressModal form').attr('action', $(this).attr('href'));
    });
});

// Set default address
function setDefaultAddress(addressId) {
    $.post('@Url.Action("SetDefaultAddress", "Account")', { id: addressId })
        .done(function () {
            location.reload();
        })
        .fail(function () {
            alert('Error setting default address');
        });
}


function setDefaultAddress(addressId) {
    // Show loading state
    const button = $(`button[onclick="setDefaultAddress('${addressId}')"]`);
    button.prop('disabled', true);
    button.html('<i class="fa fa-spinner fa-spin"></i> Processing...');

    $.ajax({
        url: '/Account/SetDefaultAddress',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ id: addressId }),
        headers: {
            'RequestVerificationToken': $('input[name="__RequestVerificationToken"]').val()
        },
        success: function (response) {
            if (response.success) {
                // Show success message
                showToast('Default address updated successfully!', 'success');
                // Refresh the page after a short delay
                setTimeout(() => location.reload(), 1000);
            } else {
                showToast(response.message || 'Failed to update default address', 'error');
                button.prop('disabled', false).html('<i class="fa fa-check-circle"></i> Set Default');
            }
        },
        error: function (xhr) {
            const errorMessage = xhr.responseJSON?.message || 'An error occurred';
            showToast(errorMessage, 'error');
            button.prop('disabled', false).html('<i class="fa fa-check-circle"></i> Set Default');
        }
    });
}

// Delete Address Confirmation
$(document).ready(function () {
    // Initialize all delete buttons
    $('.delete-address-btn').click(function (e) {
        e.preventDefault();
        var addressId = $(this).data('address-id');
        $('#deleteAddressModal-' + addressId).modal('show');
    });

    // Handle the actual delete form submission
    $('.delete-address-form').submit(function (e) {
        e.preventDefault();
        var form = $(this);

        $.ajax({
            url: form.attr('action'),
            type: 'POST',
            data: form.serialize(),
            success: function (response) {
                if (response.success) {
                    showToast('Address deleted successfully!', 'success');
                    $('#deleteAddressModal-' + response.addressId).modal('hide');
                    // Refresh the page after 1 second
                    setTimeout(function () {
                        location.reload();
                    }, 1000);
                } else {
                    showToast('Error: ' + response.message, 'error');
                }
            },
            error: function (xhr, status, error) {
                showToast('Error deleting address', 'error');
            }
        });
    });
});

}