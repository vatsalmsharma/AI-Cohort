import pandas as pd 
import streamlit as st 

from datetime import datetime
import os
from common_modules import postgres_conn as pg

st.write("""
# Daily Routine Tracker
## Let's log and track
""")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
                                    "View Progress", "Tracking Items", 
                                    "View Database", "Log Entries", 
                                    "Upload Data File"
                                  ])

with tab1:
    st.header("Keep It Up")
    
with tab2:
    st.header("My target goals")
    # View and Create - 2 options 

    pg.cur.execute('SELECT category_name, category_value FROM category;')
    rows = pg.cur.fetchall()

    # for row in rows:
    #     print(row) # ('Wake Up', '0530', datetime.datetime(2025, 9, 13, 14, 25, 44, 714320), datetime.datetime(2025, 9, 13, 14, 25, 44, 714324))

    rows_df = pd.DataFrame(rows, columns=('I want to', 'Target'))
    st.write(rows_df)

    # Initialize session state
    if "add_mode" not in st.session_state:
        st.session_state.add_mode = False
    if "data" not in st.session_state:
        st.session_state.data = []

    category_name, category_value = None, None

    # If not in add mode, show Add button
    if not st.session_state.add_mode:
        if st.button("Add Goal"):
            st.session_state.add_mode = True
    # If in add mode, show input fields with Save and Cancel
    else:
        category_name = st.text_input("My new goal is")
        category_value = st.text_input("My target is")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save"):
                st.session_state.data.append((category_name, category_value))
                st.session_state.add_mode = False
        with col2:
            if st.button("Cancel"):
                st.session_state.add_mode = False

    if st.session_state.data:
        pg.cur.execute(""" 
        INSERT INTO category (category_name, category_value, create_datetime, update_datetime) 
        VALUES(%s, %s, %s, %s)""",
        (category_name, category_value, datetime.now(),datetime.now(),)
        )

        pg.conn.commit()

        st.session_state.add_mode = False
        st.session_state.data = []

with tab3:
    st.header("Database Tables")
    
    pg.cur.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema NOT IN ('pg_catalog', 'information_schema');
                    """)
    rows = pg.cur.fetchall()

    rows_df = pd.DataFrame(rows, columns=('Table Name',))

    table_names = st.dataframe(
        rows_df,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
    )

    tbl = table_names.selection.rows
    if len(tbl) > 0:
        filtered_df = rows_df.iloc[tbl]
        tbl_name = filtered_df.iloc[0]["Table Name"]

        query = 'SELECT count(*) FROM ' + tbl_name + ' ;'
        pg.cur.execute(query)
        rows = pg.cur.fetchall()
        tbl_count = (rows[0][0])
        st.write("Record count of table '" + tbl_name + "' is " + str(tbl_count))

        query = 'SELECT * FROM ' + tbl_name + ' LIMIT 10;'
        pg.cur.execute(query)
        rows = pg.cur.fetchall()

        query = "SELECT column_name FROM information_schema.columns WHERE table_name = '" + tbl_name + "';"
        pg.cur.execute(query)
        cols = pg.cur.fetchall()
        col_df = pd.DataFrame(cols)
        col_name = tuple(col_df[0].to_list())
        # print(col_name)
        rows_df = pd.DataFrame(rows, columns=col_name)
        st.write(rows_df)

        if tbl_count > 10:   
            st.write('Note : Displaying max 10 rows')


with tab4:
    st.header("Record Progress")
    # st.session_state.inputs = {}
    # query = "SELECT distinct category_name FROM category;"
    # pg.cur.execute(query)
    # rows = pg.cur.fetchall()
    # rows_df = pd.DataFrame(rows)
    # cat_name = rows_df[0].to_list()
    # cat_len = len(cat_name)

    # # --- session state initialization ---
    # if "saved_entries" not in st.session_state:
    #     st.session_state.saved_entries = []
    # if "show_toast" not in st.session_state:
    #     st.session_state.show_toast = False

    # for i, _ in enumerate(cat_name):
    #     key = f"input_{i}"
    #     if key not in st.session_state:
    #         st.session_state[key] = ""

    # if st.session_state.show_toast:
    #     try:
    #         st.toast("✅ Data saved")   # newer Streamlit has st.toast
    #     except Exception:
    #         st.success("✅ Data saved") # fallback
    #     st.session_state.show_toast = False  # clear flag so it shows only once

    # for i, name in enumerate(cat_name):
    #     st.text_input(f"Value for {name}", key=f"input_{i}")

    # log_date = st.date_input(
    #                         "Log Date",
    #                         "today",
    #                         format="YYYY-MM-DD",
    #                         )
    # # print(log_date, type(log_date)) # 2025-09-14 <class 'datetime.date'>

    # # Buttons
    # col1, col2 = st.columns([1, 1])
    # if col1.button("Save"):
    #     # collect inputs
    #     entry = {name: st.session_state[f"input_{i}"] for i, name in enumerate(cat_name)}
    #     st.session_state.saved_entries.append(entry)

    #     # clear each input's session_state value
    #     st.session_state.clear()

    #     # set flag to show toast after rerun, then rerun so UI reflects cleared inputs
    #     st.session_state.show_toast = True
    #     # st.experimental_rerun()

    # if col2.button("Cancel"):
    #     # clear inputs and rerun
    #     st.session_state.clear()
    #     # for i in range(len(cat_name)):
    #     #     st.session_state[f"input_{i}"] = ""
    #     # st.experimental_rerun()

    # # if st.session_state.saved_entries:
    # #     st.subheader("Saved entries")
    # #     for idx, e in enumerate(st.session_state.saved_entries, 1):
    # #         st.write(f"{idx}. {e}")

    # if st.session_state:
    #     print('here')
    #     print(st.session_state)
    # #     pg.cur.execute(""" 
    # #     INSERT INTO category (category_name, category_value, create_datetime, update_datetime) 
    # #     VALUES(%s, %s, %s, %s)""",
    # #     (category_name, category_value, datetime.now(),datetime.now(),)
    # #     )

    # #     pg.conn.commit()

    # #     st.session_state.add_mode = False
    # #     st.session_state.data = []

with tab5:
    st.header('Bulk Data Upload')
    uploaded_file = st.file_uploader("Choose a file", accept_multiple_files = False)
    
    if uploaded_file is not None:
        file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type}
        st.write(file_details)
        save_path = os.path.join("data")
        
        with open(os.path.join("Uploaded_Files",uploaded_file.name),"wb") as f: 
            f.write(uploaded_file.getbuffer())         
        
        st.success("Saved File")

    # if uploaded_file is not None:




# Close cursor and communication with the database
# pg.cur.close()
# pg.conn.close()