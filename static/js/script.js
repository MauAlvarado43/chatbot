let messages = []

const onKeyPress = (event, element) => {
    if(event.charCode == 13)
        onSend()
}

const onSend = () => {

    const text_input = $('#message')
    const text = text_input.val()

    if(text.length == 0)
        return

    appendMessage(text, "USER")
    getBotMessage(text)

    text_input.val("")

}

const waitMessage = () => {
    
    $("#message-box").append(`
        <div class="message-container" id="wait-message">
            <div class="bot-message message">
                <center>
                    <div class="row">
                        <center>
                            <div class="lds-dual-ring"></div>
                        </center>
                    </div>
                    <div>
                        Escribiendo...
                    </div>
                </center>
            </div>
        </div>
    `)

}

const disposeWaitMessage = async () => {

    await new Promise(
        (resolve, reject) => {
            $("#wait-message").fadeTo(1000, 0, () => {

                let contentToRemove = document.querySelectorAll("#myid")
                $(contentToRemove).remove()

                resolve()

            })
        }
    )

}

const appendMessage = (text, type) => {

    if(type == "BOT")
        $("#message-box").append(`
            <div class="message-container">
                <div class="bot-message message">
                    ${text}
                </div>
            </div>
        `)
    else 
        $("#message-box").append(`
            <div class="message-container">
                <div class="user-message message">
                    ${text}
                </div>
            </div>
        `)
    
    $("#message-box").animate({ scrollTop: $("#message-box").prop("scrollHeight")}, 0)

}

const getBotMessage = (message) => {

    $.ajax({
        url: `/bot`,
        type: "GET",
        contentType: "application/json",
        data: {
            msg: message
        },
        beforeSend: () => {
            // waitMessage()
        },
        success: async (data) => {
            // await disposeWaitMessage()
            appendMessage(data["message"], "BOT")
        },
        error: (data) => {
            console.log(data)
        }
    })

}