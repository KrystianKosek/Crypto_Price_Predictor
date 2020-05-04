$(function () {
    $("#curr").on("change", function () {
        var curr = this.value;
        var prefix = curr == "usd";
        var sign = curr == "usd" ? "$" : "zł";
        $(".price").each(function () {
            $(this).text(
                (prefix ? sign : "") +
                $(this).data(curr) +
                (prefix ? "" : sign)
            );
        })
    }).change();
});