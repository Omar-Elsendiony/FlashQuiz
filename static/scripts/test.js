var selectedItem = null;
var question_index = 0;
var selectedItems = new Array();

function optionSelected(element) {
    // console.log(element)
    if (question_index == selectedItems.length){
        selectedItems.push(null)
    }

    if (selectedItems[question_index] != null) {
        selectedItems[question_index].style.borderColor = "#84c5fe";
        selectedItems[question_index].style.backgroundColor = "white";
        if (selectedItems[question_index] == element) {
            selectedItems[question_index] = null;
            window.choices_selected[question_index] = null
            return;
        }
    }
    element.style.backgroundColor = "lightgreen";
    element.style.borderColor = "green";

    selectedItems[question_index] = element;

    console.log(element.childNodes[3].innerHTML)
    window.choices_selected[question_index] = element.childNodes[3].innerHTML
    console.log(window.choices_selected)
}

setTimeout(() => {
    window.choices_selected = new Array(quiz_questions.length).fill(null);
    // window.choices_selected = new Array(quiz_questions.length).fill(null);



    optionsContainer = document.querySelectorAll('.option')


    options = document.querySelectorAll('.option p')

    questionText = document.getElementsByClassName('que_text')[0]
    numberQuestion = document.getElementsByClassName('numberQuestion')[0]

    document.getElementById('startButton').addEventListener('click',
        function(event) {
            // Handle the form data
            event.preventDefault();
            document.querySelector('.quiz_info').style.display = "none";
            document.querySelector('.Quiz_Start').style.display = "block";
            if (question_index == quiz_questions.length - 1){
                document.getElementById('submitButton').style.display = "block";
                document.getElementById('next').style.display = "none";
            }
            else{
                document.querySelector('#next').style.display = "block";
            }

            questionText.innerHTML = quiz_questions[question_index]
            for (let i = 0; i < options.length; i++) {
                options[i].innerHTML = quiz_questions_choices[question_index][i]
            }

            numberQuestion.innerHTML = "Question " + (question_index + 1) + " of " + quiz_questions.length
            selectedItem = null
    });
    
    document.getElementById('next').addEventListener('click',
        function(event) {
            var question = document.querySelector('.que_text').value;
            if (choices_selected[question_index] == null){
                alert("Please select an option")
                return;
            }
            question_index += 1  /////// increasing question index
            numberQuestion.innerHTML = "Question " + (question_index + 1) + " of " + quiz_questions.length

            // populate the new population
            questionText.innerHTML = quiz_questions[question_index]
            for (let i = 0; i < options.length; i++) {
                options[i].innerHTML = quiz_questions_choices[question_index][i]
            }
            if (question_index == quiz_questions.length - 1){
                document.getElementById('next').style.display = "none";
                document.getElementById('submitButton').style.display = "block";
            }

            numberQuestion.innerHTML = "Question " + (question_index + 1) + " of " + quiz_questions.length
            selectedItem = null

            for (let i = 0; i < optionsContainer.length; i++) {
                if (window.selectedItems[question_index] == optionsContainer[i]){
                    optionsContainer[i].style.backgroundColor = "lightgreen";
                    optionsContainer[i].style.borderColor = "green";
                }
                else{
                    optionsContainer[i].style.backgroundColor = "white";
                    optionsContainer[i].style.borderColor = "#84c5fe";
                }
            }

            console.log(window.selectedItems)

        }
        
    );

    document.getElementById('previousButton').addEventListener('click',
        function(event) {
            var question = document.querySelector('.que_text').value;
            if (choices_selected[question_index] == null){
                alert("Please select an option")
                return;
            }
            if (question_index == 0){
                document.querySelector('.quiz_info').style.display = "block";
                document.querySelector('.Quiz_Start').style.display = "none";
                document.querySelector('#next').style.display = "none";
                return
            }
            else if(question_index == quiz_questions.length - 1){
                document.getElementById('submitButton').style.display = "none";
                document.getElementById('next').style.display = "block";
            }

            question_index -= 1  //// decreasing question index
            
            // populate the new population
            questionText.innerHTML = quiz_questions[question_index]
            for (let i = 0; i < options.length; i++) {
                options[i].innerHTML = quiz_questions_choices[question_index][i]
            }

            for (let i = 0; i < optionsContainer.length; i++) {
                if (window.selectedItems[question_index] == optionsContainer[i]){
                    optionsContainer[i].style.backgroundColor = "lightgreen";
                    optionsContainer[i].style.borderColor = "green";
                }
                else{
                    optionsContainer[i].style.backgroundColor = "white";
                    optionsContainer[i].style.borderColor = "#84c5fe";
                }
            }

            numberQuestion.innerHTML = "Question " + (question_index + 1) + " of " + quiz_questions.length
            // selectedItem = null
            console.log(window.selectedItems)
        }
        
    );
    

    function submitContent() {
        let headers = new Headers();
        headers.append('Content-Type', 'application/json');
        // headers.append('Access-Control-Allow-Origin', 'http://127.0.0.1:5000');
        headers.append('Access-Control-Allow-Credentials', 'true');
    
        fetch("/test/" + quiz_id, {
                method: "POST",
                body: JSON.stringify({
                    "choices": window.choices_selected,
                }),
                headers: headers
            })
            .then((response) => response.json())
            .then((json) => 
                document.getElementsByClassName('end')[0].innerHTML = "<h2> You have got " + json["mark"] + " out of " + quiz_questions.length +" </h2>"
        );
    }

    document.getElementById('submitButton').addEventListener('click',
        function(event) {
            if (choices_selected[question_index] == null){
                alert("Please select an option")
                return;
            }
            /////////// start submitting the content of the question, options and title /////////////
            submitContent()
            document.querySelector('.Quiz_Start').style.display = "none";
            document.querySelector('.end').style.display = "block";
    });


    console.log(quiz_questions)
    console.log(quiz_questions_choices)
}, 1000);

















/////////////////////////////////////////////////////
//////////////// ANIMATE RUBIK //////////////////////
////////////////////////////////////////////////////

setTimeout(() => {
    var start = true
    var direction = "down";
    function downToUp() {
        $("#floatingRubik").animate({ top: '-=50%' }, 10000, function() {
                animateElement(); 
        })};


    function upToDown() {
        $("#floatingRubik").animate({ top: '+=50%' }, 10000, function() {
                animateElement();
        })};

    function animateElement() {
        var parentElement = document.getElementsByClassName('playing_rubik')[0];
        visibilityParent = parentElement.checkVisibility();
        // console.log(visibilityParent)
        if (visibilityParent == false){
            return
        }

        var element = document.getElementById('floatingRubik');

        // console.log(screen.height)
        
        var position = element.getBoundingClientRect();
        var x = position.left;
        var y = position.top;
        // console.log(y)
        
        if (start == true) {
            start = false;
            upToDown();
        }
        else{
            // console.log("else")
            if (y > 0.3 * screen.height ) {
                direction = "up";
                // rightToLeft();
            }
            if (y <= 0.3 * screen.height) {
                direction = "down"
                // leftToRight();
            }
            if (direction == "down") {
                upToDown();
            }
            else{
                downToUp();
            }
        }
    }
    // Start the animation
    animateElement();

}, 50);
