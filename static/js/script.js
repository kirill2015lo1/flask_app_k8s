$(document).ready(function() {
    $('form').on('submit', function(e) {
        e.preventDefault();  // Отменить стандартную отправку формы

        var formData = new FormData(this);  // Получаем все данные формы

        $.ajax({
            url: '/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // Перезагружаем ленту постов без перезагрузки страницы
                $('#posts').html($(response).find('#posts').html());
                $('form')[0].reset();  // Очистить форму
            },
            error: function(xhr, status, error) {
                alert('Something went wrong. Please try again!');
            }
        });
    });
});
