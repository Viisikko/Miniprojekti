function generate_index() {
    const year = document.querySelector('[name="year"]').value;
    const authors = document.querySelector('[name="author"]').value.split(",");
    const generated_index = authors[0].replaceAll(" ", "") + year;
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


async function autofill_doi() {
    function autofill_field(id, from) {
        if ((from[id] != undefined) && (from[id] != null)){
            document.querySelector('[name="'+id+'"]').value = from[id]
        }
    }

    if (document.querySelector('[name="doi"]').value.length == 0){
        return
    }

    const res = await fetch("/metadata?" + new URLSearchParams({
        doi: document.querySelector('[name="doi"]').value
    }))

    if (!res.ok){
        return
    }

    
    let api_json = await res.json()
    
    
    document.querySelector("div.doi-warning").setAttribute("show", api_json["existing"])

    if(api_json["authors"] != null){
        api_json["authors"] = api_json["authors"].join(", ")
    }

    autofill_field("title", api_json)
    autofill_field("url", api_json)
    autofill_field("year", api_json)
    autofill_field("journal", api_json)
    autofill_field("publisher", api_json)
    autofill_field("author", api_json)
    autofill_field("doi", api_json)

    generate_index_request()

}

function handle_reftype() {
    document.querySelector("form.add_reference").setAttribute("rtype", document.querySelector("[name='type']").value)
}