import streamlit as st

st.title("Simple Calculator")
st.write("You can enter as many numbers as you like when adding.")

st.sidebar.title("Select operation")
operation = st.sidebar.selectbox("Choose operation:", ("add", "subtract", "multiply", "divide"))

numbers = []
result = None

if operation == "add":
    numbers_input = st.text_area(
        "Enter numbers separated by commas",
        value="0, 0",
        help="You can type 10, 20, 30, ..."
    )

    for part in numbers_input.split(","):
        cleaned = part.strip()
        if cleaned:
            try:
                numbers.append(float(cleaned))
            except ValueError:
                st.error(f"'{cleaned}' is not a valid number")
                numbers = []
                break
else:
    num1 = st.number_input("Enter first number", value=0.0)
    num2 = st.number_input("Enter second number", value=0.0)

if st.button("Calculate"):
    if operation == "add":
        if numbers:
            result = sum(numbers)
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        if num2 == 0:
            st.error("Cannot divide by zero")
        else:
            result = num1 / num2

    if result is not None:
        st.success(f"the result is {result}")
