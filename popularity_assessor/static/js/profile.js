function submitInstaToken() {
    let token = $("#insta-token").val();

    if (token) {

        const csrftoken = getCookie('csrftoken');

        console.log(csrftoken);

        $.ajax({
            type: "post",
            url: "/popularity_assessor/connect-insta/",
            data: JSON.stringify({ token: token }),
            dataType: "json",
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            success: function (response) {
                window.alert("Token added");
                $("#token-pop-up").addClass("d-none");
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });

    } else {
        window.alert("Please provide the dev token for instagram")
    }
}