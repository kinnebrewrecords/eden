import streamlit as st


st.set_page_config(
    page_title="Eden Help",
    layout="wide"
)

st.title("How can Eden help?")
st.caption(
    "Create estimates, save them to projects, and review material takeoffs."
)

st.subheader("Start a project")

st.markdown("""
1. Create a project: `create project Demo House`
2. Eden selects it automatically.
3. Ask Eden to estimate an item.
4. Use `show project` to review saved estimates and materials.
""")

st.subheader("Concrete")

st.markdown("""
- `estimate a 20 x 20 slab, 6 inches thick`
- `estimate a concrete footing`
- `estimate a concrete beam`
- `estimate a patio`
""")

st.subheader("Lumber and roofing")

st.markdown("""
- `estimate a framed wall`
- `estimate roof sheathing`
- `estimate shingles`
""")

st.subheader("Interior finishes")

st.markdown("""
- `estimate wall drywall`
- `estimate batt insulation`
- `estimate interior paint`
""")

st.subheader("Mechanical, electrical, and plumbing")

st.markdown("""
- `estimate outlets`
- `estimate pex pipe`
- `estimate ductwork`
""")

st.subheader("Project commands")

st.markdown("""
- `create project <project name>`
- `select project <project name>`
- `show project`
- `delete project <project name>`
""")

st.subheader("During an estimate")

st.markdown("""
- Type `cancel` to stop.
- Type `change to <estimate type>` to switch estimates.
- Eden will ask for any missing measurements or plan details.
""")