# import the streamlit library
import streamlit as st
#import locale

# App title
st.title('Project Percent Complete and Revenue to be Recognized')

# Computaion formulas
formulas_defined = """
<div style="border: 2px solid #336699; padding: 10px; border-radius: 5px;">
    <p><strong>Percent Complete fomula: ITD Cost / Project Budget.</strong></p>
    <p><strong>Revenue to be Recognized formula: Funded Value * Percent Complete.</strong></p>
</div>
"""
# Describe the formulas
st.markdown(formulas_defined, unsafe_allow_html=True)
st.text("")
st.text("")

# User to enter funded contract value
project_funded_value = st.number_input(
     label = "Project Funded Value",
     help = "Enter project's contracted funded value")

# User to enter actual cost
ctd_cost = st.number_input(
     label = "Project ITD Cost",
     help = "Enter project's inception to date actual cost to date")
 
# User to enter total project budget
project_budget = st.number_input(
     label = "Project Budget",
     help = "Enter project's budget value greater than zero")

percent_complete = 0

#compute percentage complete
def compute_percent_complete():
    try:
        percent_complete = ctd_cost / project_budget
        if(percent_complete <= 0 ):
            percent_complete = 0
        elif(percent_complete <= 1):
            percent_complete = percent_complete * 100
        elif(percent_complete > 1):
            percent_complete = 1 * 100
    except ZeroDivisionError:
        st.text("Enter a value greater than zero for the budget")

    return percent_complete

def compute_revenue():
    revenue = project_funded_value * percent_complete / 100
    return revenue

#def format_amount(res: int) -> str:
    
    #  Format to two decimal digits currency as string
    #locale.setlocale(locale.LC_ALL, "en_CA.UTF-8")
    #return locale.currency(res, grouping=True)


# When button is pressed
if(st.button('Calculate Percent Complete')):
        #Validate that project budget entered is greater than zero
        if(project_budget <=0):
             custom_warning_message = """
                <div style="background-color: #ffcccc; padding: 10px; border: 1px solid #ff0000; border-radius: 5px;">
                <p style="color: #ff0000; font-weight: bold;">ERROR: 
                Budget must be greater than zero.</p>
                </div>
                """

            # Display the custom warning message
             st.markdown(custom_warning_message, unsafe_allow_html=True)
             #st.warning("Error: Budget must be greater than zero")
             #warning_message =  "Error: Budget must be greater than zero."
             #st.markdown(f'<p style="color: red; font-weight: bold;">   {warning_message}</p>', unsafe_allow_html=True)
        else:
             percent_complete = round(compute_percent_complete(),2)
             revenue = compute_revenue()
             # Format the revenue as currency with two decimal digits
             # DELETE LATERrevenue_formatted = format_amount(2)
             st.warning(f"Project Percent Complete is: {percent_complete:.2f}%")
             st.warning(f"ITD revenue to be recognized is: $ {revenue:.2f}")

             # DELETE LATER - st.text(f"ITD revenue to be recognized is: {revenue_formatted}")