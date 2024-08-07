document.getElementById("url-form").addEventListener("submit", function(event) {
    event.preventDefault();
            
    var url = document.getElementById("url-input").value;

    var errorMsg = document.getElementById("url-error");
    if (!url.trim()) {
        errorMsg.style.display = "block";
        var resultDiv = document.getElementById("result");
        resultDiv.innerText = "";
        resultDiv.className = "";
        return false; 
    } else {
        errorMsg.style.display = "none"; 
    }
            
    fetch("/predict", {
        method: "POST",
        body: new URLSearchParams({
            url: url
        }),
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    })
    .then(response => response.json()) 
    .then(data => {
        var resultDiv = document.getElementById("result");
        resultDiv.innerText = data.prediction;

        if (data.prediction === "This URL is safe") {
            resultDiv.classList.add("benign");
            resultDiv.classList.remove("non-benign");
        } else {
            resultDiv.classList.add("non-benign");
            resultDiv.classList.remove("benign");
        }
        })
    .catch(error => {
        console.error("Error:", error);
    });
});
