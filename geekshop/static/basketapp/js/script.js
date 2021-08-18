// срабатывает если стр полностью загружена
window.onload = function () {
    // если кликаем вызываем функцию
    $('.basket_list').on('click', 'input[type=number]', function (event) {
        var t_href = event.target;
        console.log(t_href);
        // у jquary вызываем метод
        $.ajax({
            url: "/basket/edit/" + t_href.name + "/" + t_href.value + "/",

            success: function (data) {
                // переписываем данные в html странице
                $('.basket_list').html(data.result);
            },
        });
        event.preventDefault(); // спасает от всплытия
    });
}
