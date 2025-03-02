from flask import Flask, render_template, request
from mark_six_utils import (
    generate_initital_mark_six_list,
    generate_17_units,
    get_first_8_units,
    get_second_8_units,
    get_last_1_unit,
    validate_count,
    recursive_generate,
    generate_n1_to_n7,
    get_m6_result_by_index
)
import json
import socket

app = Flask(__name__)


@app.template_filter("check_values")
def check_values(value, n1, n2, n3, n4, n5, n6):
    result = False
    if (
        str(value) == str(n1)
        or str(value) == str(n2)
        or str(value) == str(n3)
        or str(value) == str(n4)
        or str(value) == str(n5)
        or str(value) == str(n6)
    ):
        result = True
    return result


@app.template_filter("check_value_special")
def check_value_special(value, n7):
    result = False
    if str(value) == str(n7):
        result = True
    return result


@app.template_filter("format_number_3")
def format_number_3(value):
    value = f"{value:,}"
    return value


@app.template_filter("format_number_round")
def format_number_round(value, n=0):
    value = round(value, n)
    return value


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/get_mark_six")
def get_mark_six():
    units, e1, e2, e3 = generate_17_units()

    response = ""
    for unit in units:
        response += str(unit) + "<br>"

    # for i in range(49):
    #     response += f"<br> {str(i+1)} : {str(validate_dict.get(i+1))}"
    return response


@app.route("/mark_six", methods=["GET", "POST"])
def mark_six():
    display_overlay = False
    ip_address = request.remote_addr
    try:
        # Perform a reverse DNS lookup to get the hostname
        client_hostname = socket.gethostbyaddr(ip_address)[0]
    except socket.herror:
        client_hostname = "Unknown Hostname"
    print(f"Client IP address: {ip_address}, Client Computer Name: {client_hostname}")

    # initial dictionary
    match_dict = {
        "0": 0,
        "0.5": 0,
        "1": 0,
        "1.5": 0,
        "2": 0,
        "2.5": 0,
        "3": 0,
        "3.5": 0,
        "4": 0,
        "4.5": 0,
        "5": 0,
        "5.5": 0,
        "6": 0,
    }
    if request.method == "GET":
        results, e1, e2, e3 = generate_17_units()
        results_json = json.dumps(results)
        # print("results_json: ", results_json)
        return render_template(
            "mark_six.html",
            results=results,
            results_json=results_json,
            match_dict=match_dict,
            try_count=10,
            e1=e1,
            e2=e2,
            e3=e3,
            display_overlay=display_overlay,
        )

    if request.method == "POST":
        n1 = request.values.get("n1")
        n2 = request.values.get("n2")
        n3 = request.values.get("n3")
        n4 = request.values.get("n4")
        n5 = request.values.get("n5")
        n6 = request.values.get("n6")
        n7 = request.values.get("n7")
        e1 = request.values.get("e1")
        e2 = request.values.get("e2")
        e3 = request.values.get("e3")
        type = request.values.get("type")
        results_json = request.values.get("results_json")
        try_count = 100
        try:
            # Attempt to convert the string to an integer
            try_count = int(request.values.get("try_count")) or 100
        except ValueError:
            # Handle the error if conversion fails
            pass
        except TypeError:
            # Handle the error if conversion fails
            pass

        # print("results_json: ", results_json)
        results = json.loads(results_json)
        # print(" ")
        print("Request: ", type, try_count, n1, n2, n3, n4, n5, n6, n7)
        # print("results_json: ", results_json)

        # determinate the action by type
        if type == "check":
            pass
        elif type == "regenerate":
            results, e1, e2, e3 = generate_17_units()
            results_json = json.dumps(results)
        elif type == "regenerate_auto":
            if (
                n1 == ""
                and n2 == ""
                and n3 == ""
                and n4 == ""
                and n5 == ""
                and n6 == ""
                and n7 == ""
            ):
                n1, n2, n3, n4, n5, n6, n7 = generate_n1_to_n7()
            try_count = recursive_generate(
                match_dict, try_count, n1, n2, n3, n4, n5, n6, n7
            )

        return render_template(
            "mark_six.html",
            results=results,
            results_json=results_json,
            match_dict=match_dict,
            try_count=try_count,
            n1=n1,
            n2=n2,
            n3=n3,
            n4=n4,
            n5=n5,
            n6=n6,
            n7=n7,
            e1=e1,
            e2=e2,
            e3=e3,
            display_overlay=display_overlay,
        )


@app.route("/get_mark_six_results", methods=["GET", "POST"])
def get_mark_six_results():
    if request.method == "POST":
        result_index = request.values.get("result_index")
    result = get_m6_result_by_index(int(result_index))

    return result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999, debug=True)
