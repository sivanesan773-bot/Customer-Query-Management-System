import streamlit as st
import mysql.connector as mc
from datetime import date
import re
import cred
mydb = mc.connect(host=cred.sqlHost,user=cred.sqlUser,password=cred.sqlPword,database=cred.sqlDatabase)

mycursor = mydb.cursor()
query_details = []

def finel_update(resolution,final_status,qid):
    resolve_date = str(date.today())
    sql3 = "UPDATE cqms.synthetic_client_queries SET  date_closed = '"+resolve_date+"',Resolution_Provided = '"+resolution+"',status='"+final_status+"' WHERE query_id = '"+qid+"'"
    print("sql3 final : "+sql3)
    mycursor.execute(sql3)
    mydb.commit()
    # st.success("Resolution Updated successfully")


def get_quey_details(qid):
    sql2 = "select query_heading,query_description  from cqms.synthetic_client_queries where query_id='"+qid+"'"
    print("sql2 : "+sql2)
    mycursor.execute(sql2)
    for x in mycursor :
        query_details.extend(list(x))
    return query_details



def genrate_query_id() :
    sql1 = "SELECT query_id FROM cqms.synthetic_client_queries ORDER BY query_id DESC LIMIT 1"
    mycursor.execute(sql1)

    for x in mycursor :
        string_id = x
        s = string_id[0]  # extract the string from tuple
        number = re.sub(r'\D', '', s)  # remove all non-digits
        newQueryId = "Q00"+str(int(number)+1)
        return(newQueryId)

def support_page():
    st.title("Support Page")
    if "show_resolution_form" not in st.session_state:
        st.session_state.show_resolution_form = False

    with st.form(key="query_form"):
        status = st.selectbox("Status", ("Open", "Closed"))
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        if status == "Open":
            st.session_state.show_resolution_form = True
        else:
            st.session_state.show_resolution_form = False

    if st.session_state.show_resolution_form:
        try:
    # Fetch open queries
            sql = """
                SELECT query_id, client_email, client_mobile, query_heading, query_description, date_raised
                FROM cqms.synthetic_client_queries 
                WHERE status = 'Open' 
                ORDER BY query_id ASC 
                LIMIT 10
            """
            mycursor.execute(sql)
            results = mycursor.fetchall()

            st.subheader("List Of Open Queries")

            if results:
                for row in results:
                    query_id, email, mobile, heading, description, date_raised = row

                    # Card UI
                    with st.container():
                        st.markdown(
                            f"""
                            <div style="border:1px solid #ddd; border-radius:10px; padding:15px; margin-bottom:15px;
                                        box-shadow: 2px 2px 8px rgba(0,0,0,0.1); background-color:#f9f9f9;">
                                <h4 style="margin:0; color:#2C3E50;">{heading}</h4>
                                <p><b>Query ID:</b> {query_id}</p>
                                <p><b>Email:</b> {email}</p>
                                <p><b>Mobile:</b> {mobile}</p>
                                <p><b>Description:</b> {description}</p>
                                <p><b>Date Raised:</b> {date_raised}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    # Inline resolution form per card
                    with st.form(key=f"resolution_form_{query_id}"):
                        Resolution = st.text_area(f"Resolution for {query_id}", key=f"res_{query_id}")
                        finalstatus = st.selectbox(f"Final Status for {query_id}", ["Closed"], key=f"status_{query_id}")
                        final_submit_button = st.form_submit_button("Update")

                        if final_submit_button:
                            if Resolution and finalstatus:
                                resolve_date = str(date.today())
                                sql3 = """
                                    UPDATE cqms.synthetic_client_queries 
                                    SET date_closed = %s, Resolution_Provided = %s, status = %s
                                    WHERE query_id = %s
                                """
                                values = (resolve_date, Resolution, finalstatus, query_id)
                                mycursor.execute(sql3, values)
                                mydb.commit()
                                st.success(f"Query {query_id} updated successfully")
                            else:
                                st.warning("Please fill out all the fields.")
            else:
                st.info("No open queries found.")

        except Exception as e:
            st.error(f"Error: {e}")

    if submit_button and status == "Closed":
        try:
            sql = """
                SELECT query_id,client_email,client_mobile,query_heading,query_description,status,date_raised,date_closed,Resolution_Provided 
                FROM cqms.synthetic_client_queries 
                WHERE status = 'Closed'  
                ORDER BY query_id DESC 
                LIMIT 10
            """
            mycursor.execute(sql)
            results = mycursor.fetchall()
            st.subheader("List Of Recently Closed Queries")
            if results:
             for row in results:
                 query_id, email, mobile, heading, description,status,Opened_date, date_closed,resolution  = row
                 with st.container():
                    st.markdown(
                        f"""
                        <div style="border:1px solid #ddd; border-radius:10px; padding:15px; margin-bottom:15px;
                                    box-shadow: 2px 2px 8px rgba(0,0,0,0.1); background-color:#f9f9f9;">
                            <h4 style="margin:0; color:#2C3E50;">{heading}</h4>
                            <p><b>Query ID:</b> {query_id}</p>
                            <p><b>Email:</b> {email}</p>
                            <p><b>Mobile:</b> {mobile}</p>
                            <p><b>Status:</b> {status}</p>
                            <p><b>Description:</b> {description}</p>
                            <p><b>Issue raised Date:</b> {Opened_date}</p>
                            <p><b>Date Closed:</b> {date_closed}</p>
                            <p><b>Resolution:</b> {resolution}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("No closed queries found.")
        #     st.write(" | ".join(str(row)[2:7] for row in results))
        # except Exception as e:
        #     st.error(f"Error: {e}")
        except Exception as e:
          st.error(f"Error: {e}")




def client_page():
    print("client page entry")
    st.markdown(
        """
        <h1 style='text-align: center; color: #2C3E50;'>
            Please share your Query
        </h1>
        <hr>
        """,
        unsafe_allow_html=True
    )
    # st.title("Please share your Query")

    with st.form(key='query_form'):
        email = st.text_input("Email Id")
        mobile_number = st.text_input("Mobile Number",max_chars=10)
        query_heading = st.text_input("Query Heading")
        query_description = st.text_area("Query Description")

        submit_button = st.form_submit_button("Submit")

    if submit_button:
        # Check if the inputs are not empty
        if email and mobile_number and query_heading and query_description:
            try : 
            #   mycursor.execute("update cqms.synthetic_client_queries set client_mobile = '8870482834' where query_id = 'Q0001'")
              sql = """insert into cqms.synthetic_client_queries (query_id, client_email, client_mobile, query_heading, query_description, status, date_raised, date_closed, Resolution_Provided) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
              creation_date = str(date.today())
              quid = genrate_query_id ()
              print(quid)
              mobile_val = int(mobile_number)
              val = (quid,email,mobile_val,query_heading,query_description,"Open",creation_date,None,None)
              print("DEBUG SQL:", sql)
              print("DEBUG VAL:", val, len(val)) 
              mycursor.execute(sql,val)
              mydb.commit()
              st.success("Your query has been registered successfully!")
              print("Completed")
            except Exception as e :
              print(e)

        else:
            st.warning("Please fill out all the fields.")

def streamlite_page():
    print("entring hope page")
    st.markdown(
        """
        <style>
        .header {
            background-color: #2C3E50;
            padding: 15px;
            text-align: center;
            color: white;
            font-size: 26px;
            font-weight: bold;
            border-radius: 8px;
        }
        </style>
        <div class="header">Customer Query Management System</div>
        """,
        unsafe_allow_html=True
    )
    
    # Use session state to manage login status
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ("Client", "Support"))
        login_button = st.button("Login")

        if login_button:
            if username == cred.clientUname and password == cred.clientPword and role == "Client":
                st.session_state.logged_in = True
                st.session_state.role = "Client"
                st.success("Logged in successfully!")
                st.rerun()  # Rerun the script to show the client page
                client_page()
            elif username == cred.supportUname and password == cred.supportPword and role == "Support" :
                st.session_state.logged_in = True
                st.session_state.role = "Support"
                st.success("Logged in successfully!")
                st.rerun()
                support_page()
            else:
                st.error("Invalid username or password.")
    
    if st.session_state.logged_in:
        if st.session_state.role == "Client":
            client_page()
        elif st.session_state.role == "Support":
            support_page()

if __name__ == "__main__":
    streamlite_page()