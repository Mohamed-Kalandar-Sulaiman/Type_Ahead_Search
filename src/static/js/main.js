document.addEventListener("DOMContentLoaded", () => {
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-btn");
    const messagesDiv = document.getElementById("messages");

    const jwt = "Bearer eyJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJpZGVuaXR5Iiwic3ViIjoiNmIxN2EwMzQtOTEwNS00ODhiLTliMDEtMzkzMjdlNTMzNjMzIiwiaWF0IjoxNzM0ODc1NDI3LCJleHAiOjE4MzU4ODI0MzZ9.Xqwn_bgxrvpUbo5qKDkrolWgl0z0Ij1ek3w11pml6fm2R85YTgY_cN1hjI8VgtTdLAuJVs5uC4DZWEDUeHxpb5gM-LUzmJbbN6H9fhleG5UdsUt3ZLFYEdLh35m49Qekz7ul8vY_qEb2b3nvBRLvUTaDGjyKt57vKBsa72mBOP8M4uyz5ap_S9oew5IpNHv0k8m8TEzFxRpyYGo95nhTMicdlrEPU_Gmy2kgljf_YNZ_DZlG8P1vAd45IRifHixwoziAGTvpHGKZ-yULiH1TU0zqiAwt78Uw5xsx-BGK7Q-RwWE-C-FYhprZkFHz6AjQD_CTM4kbdmKEFgD2VMknug";
    const socket = new WebSocket('ws://localhost:80/api/v1/search/typeahead?Authorization=' + jwt); // WebSocket URL

    socket.onopen = () => {
        console.log("WebSocket is connected.");
        const jsonMessage = { "prefix": "" };  
        socket.send(JSON.stringify(jsonMessage)); 
    };

    socket.onmessage = (event) => {
        try {
            const message = JSON.parse(event.data);  // Parse the incoming JSON message
            console.log("Message received:", message);
        
            // Create structured HTML content
            let formattedMessage = '';
            
            // Suggestions Section
            if (message.suggestions) {
                formattedMessage += '<div class="custom-card mb-3"><div class="custom-card-body">';
                formattedMessage += '<h3 class="text-center text-warning">Suggestions</h3><ul class="custom-list">';
                message.suggestions.forEach(suggestion => {
                    formattedMessage += `
                        <li class="custom-list-item">
                            <strong>${suggestion.text}</strong>
                        </li>
                    `;
                });
                formattedMessage += '</ul></div></div>';
            }
    
            // Articles Section
            if (message.articles) {
                formattedMessage += '<div class="custom-card mb-3"><div class="custom-card-body">';
                formattedMessage += '<h3 class="text-center text-primary">Articles</h3><ul class="custom-list">';
                message.articles.forEach(article => {
                    formattedMessage += `
                        <li class="custom-list-item">
                            <strong>${article.title}</strong>
                            <p class="tags text-muted">Tags: ${article.tags.join(', ')}</p>
                        </li>
                    `;
                });
                formattedMessage += '</ul></div></div>';
            }
        
            // Authors Section
            if (message.authors) {
                formattedMessage += '<div class="custom-card mb-3"><div class="custom-card-body">';
                formattedMessage += '<h3 class="text-center text-success">Authors</h3><ul class="custom-list">';
                message.authors.forEach(author => {
                    formattedMessage += `
                        <li class="custom-list-item">
                            <strong>${author.name}</strong>
                            <p class="tags text-muted">Writes about: ${author.writes_about.join(', ')}</p>
                        </li>
                    `;
                });
                formattedMessage += '</ul></div></div>';
            }
        
            // Publications Section
            if (message.publications) {
                formattedMessage += '<div class="custom-card mb-3"><div class="custom-card-body">';
                formattedMessage += '<h3 class="text-center text-info">Publications</h3><ul class="custom-list">';
                message.publications.forEach(publication => {
                    formattedMessage += `
                        <li class="custom-list-item">
                            <strong>${publication.name}</strong>
                            <p class="tags text-muted">Tags: ${publication.tags.join(', ')}</p>
                        </li>
                    `;
                });
                formattedMessage += '</ul></div></div>';
            }
        
            // History Section (with possible missing prefix)
            if (message.history) {
                formattedMessage += '<div class="custom-card mb-3"><div class="custom-card-body">';
                formattedMessage += '<h3 class="text-center text-danger">History</h3><ul class="custom-list">';
                message.history.forEach(item => {
                    const prefixText = item.prefix || 'No Prefix';  // Handle missing prefix
                    formattedMessage += `
                        <li class="custom-list-item">
                            ${prefixText}
                        </li>
                    `;
                });
                formattedMessage += '</ul></div></div>';
            }
        
            // Display structured message inside messagesDiv
            messagesDiv.innerHTML = formattedMessage;
        
            // Optional: Auto-scroll to the bottom
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        } catch (e) {
            console.error("Error parsing received message:", e);
        }
    };
    
    
    

    // When connection is closed
    socket.onclose = () => {
        console.log("WebSocket connection closed.");
    };

    // Send message when the button is clicked
    messageInput.addEventListener("input", () => {
        const message = messageInput.value;
        if (message) {
            const jsonMessage = { "prefix": message };  
            socket.send(JSON.stringify(jsonMessage)); 
        }
    });
});
