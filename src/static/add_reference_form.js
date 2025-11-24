function generate_index() {
    const year = document.querySelector('[name="year"]').value;
    const authors = document.querySelector('[name="author"]').value.split(",");
    const generated_index = authors.join("").replaceAll(" ", "") + year;

    document.querySelector('[name="index"]').value = generated_index;
}


function handle_reftype(){
    document.querySelector("form.add_reference").setAttribute("rtype", document.querySelector("[name='type']").value)
}