function generate_index() {
    const year = document.querySelector('[name="year"]').value;
    const authors = document.querySelector('[name="author"]').value.split(",");
    const generated_index = authors.join("").replaceAll(" ", "") + year;
    return generated_index
}

async function generate_index_request() {
    let give_up_counter = 0;
    const result = generate_index();

    while (give_up_counter < 10) {
        let index_name = result;
        if (give_up_counter != 0){
            index_name = result + "_" + give_up_counter
        }
        const res = await fetch("/index/" + index_name);
        
        if (!res.ok){
            document.querySelector('[name="index"]').value = index_name;
            break;
        }

        const result_json = await res.json()

        if (result_json["status"] == false){
            document.querySelector('[name="index"]').value = index_name;
            break
        }

        give_up_counter++;
    }
}

function handle_reftype() {
    document.querySelector("form.add_reference").setAttribute("rtype", document.querySelector("[name='type']").value)
}