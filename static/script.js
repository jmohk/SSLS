function changeValue(inputId, change) {
    var inputElement = document.getElementById(inputId);
    var newValue = parseInt(inputElement.value) + change;
    if (newValue >= 0 && newValue <= 100) {
        inputElement.value = newValue;
    }
}

document.addEventListener("DOMContentLoaded", function() {
    var amPmSelects = document.querySelectorAll(".am-pm-select");

    amPmSelects.forEach(function(select) {
        select.addEventListener("change", function() {
            var selectedValue = this.value;
            var mainDiv = this.closest(".main");
            if (selectedValue === "2") {
                mainDiv.classList.add("pm");
            } else {
                mainDiv.classList.remove("pm");
            }
            
            // Trigger change event programmatically
            var event = new Event("change");
            this.dispatchEvent(event);
        });
    });

    const toggleSwitch = document.getElementById('toggleSwitch');
    const form1 = document.querySelector('.form-1');
    const form2 = document.querySelector('.form-2');

    toggleSwitch.addEventListener('change', function() {
        if (toggleSwitch.checked) {
            form1.style.display = 'none';
            form2.style.display = 'block';
        } else {
            form1.style.display = 'block';
            form2.style.display = 'none';
        }
    });

    // Function to fetch and display the number of cars
    function updateNumCars() {
        fetch("/num_faces")
            .then(response => response.text())
            .then(data => {
                var num_cars = parseInt(data);
                if (!isNaN(num_cars)) {
                    document.querySelector(".c-r").value = "Number of cars: " + num_cars;
                } else {
                    console.error("Invalid number of cars:", data);
                }
            })
            .catch(error => console.error("Error fetching number of cars:", error));
    }

    // Event listener for the Scan number of cars button
    document.querySelector(".c-b").addEventListener("click", function() {
        window.open('/video_feed', 'Camera Feed', 'width=640,height=480');
        setTimeout(updateNumCars, 5000);
    });

    // Form-1 submission event listener
    document.getElementById("prediction-form").addEventListener("submit", function(event) {
        event.preventDefault();

        var formData = {
            values: [
                parseInt(document.getElementById("month").value),
                parseInt(document.getElementById("hour").value),
                parseInt(document.getElementById("rain").value),
                parseInt(document.getElementById("fog").value),
                parseInt(document.getElementById("am-pm").value)
            ]
        };

        fetch("/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            alert("Prediction: " + data.prediction + "\nOptimal Light: " + data.optimalLight);
        })
        .catch(error => console.error("Error submitting form:", error));
    });

    // Form-2 Submission
    document.querySelector(".form-2").addEventListener("submit", function(event) {
        event.preventDefault();
        var month = document.getElementById("month2").value;
        var hour = document.getElementById("hour2").value;
        var ampm = document.getElementById("am-pm2").value;
        if (ampm === "2" && hour < 12) {
            hour += 12; // Convert hour to 24-hour format for PM
        } else if (ampm === "1" && hour === 12) {
            hour = 0; // Convert 12 AM to 0 for 24-hour format
        }
        var data = {"month": month, "hour": hour};
        console.log("Form-2 data:", data); // Debugging statement
        fetch("/form-2", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log("Response from server:", data); // Debugging statement
            alert("Light Decision: " + data.light_decision);
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });
});
