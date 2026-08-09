from datetime import date

import streamlit as st

from Settings import Settings
from UserProfile import (
    load_profile,
    save_profile,
    save_avatar
)
from EdenTheme import apply_eden_theme
from Sidebar import render_sidebar
import html
from EstimatingPreferences import EstimatingPreferences
from PricingCatalog import PricingCatalog
from EdenAI import EdenAI
from AuthGate import require_eden_login


st.set_page_config(
    page_title="Settings",
    layout="wide"
)

apply_eden_theme()
require_eden_login()

st.markdown(
    """
    <style>
        .eden-settings-table {
            background: #0E1621;
            border: 1px solid #2E435E;
            border-radius: 10px;
            overflow: hidden;
        }

        .eden-settings-table table {
            border-collapse: collapse;
            color: #EAF2FF;
            width: 100%;
        }

        .eden-settings-table th {
            background: #111C2A;
            color: #7DD3FC;
            font-size: 0.8rem;
            letter-spacing: 0.04em;
            text-align: left;
        }

        .eden-settings-table th,
        .eden-settings-table td {
            border-bottom: 1px solid #223044;
            padding: 12px 14px;
        }

        .eden-settings-table tr:last-child td {
            border-bottom: none;
        }

        .eden-settings-table td:last-child {
            color: #38BDF8;
            text-align: right;
        }
    </style>
    """,
    unsafe_allow_html=True
)

render_sidebar(
    show_command_center=False,
    show_project_manager=False
)

st.title("Settings")
st.caption(
    "Manage your company profile and review Eden’s estimating defaults."
)

profile = load_profile()
preferences = EstimatingPreferences()
pricing = PricingCatalog()
pricing.add_starter_regions()


def render_settings_table(rows):
    table_rows = ""

    for row in rows:
        setting = html.escape(str(row["Setting"]))
        value = html.escape(str(row["Value"]))

        table_rows += (
            "<tr>"
            f"<td>{setting}</td>"
            f"<td>{value}</td>"
            "</tr>"
        )

    st.markdown(
        f"""
        <div class="eden-settings-table">
            <table>
                <thead>
                    <tr>
                        <th>Setting</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True
    )

all_settings = {}

for setting_name in dir(Settings):
    if setting_name.isupper():
        all_settings[setting_name] = getattr(
            Settings,
            setting_name
        )

open_pricing_setup = st.session_state.pop(
    "eden_open_pricing_setup",
    False
)

if open_pricing_setup:
    pricing_tab, profile_tab, defaults_tab = st.tabs(
        [
            "Regional Pricing",
            "Company Profile",
            "Estimating Defaults"
        ]
    )
else:
    profile_tab, defaults_tab, pricing_tab = st.tabs(
        [
            "Company Profile",
            "Estimating Defaults",
            "Regional Pricing"
        ]
    )

with profile_tab:
    st.subheader("Company Profile")
    st.caption(
        "This information appears across your Eden workspace and reports."
    )

    with st.expander(
            "Company information and profile image",
            expanded=True
    ):
        with st.form("company_profile_form"):
            name = st.text_input(
                "Your name",
                value=profile.get("name", "")
            )

            company = st.text_input(
                "Company name",
                value=profile.get("company", "")
            )

            phone = st.text_input(
                "Phone",
                value=profile.get("phone", "")
            )

            email = st.text_input(
                "Email",
                value=profile.get("email", "")
            )

            address = st.text_area(
                "Business address",
                value=profile.get("address", "")
            )

            profile_regions = pricing.list_regions()
            current_region = profile.get("default_region", "")
            region_index = 0

            if current_region in profile_regions:
                region_index = profile_regions.index(current_region)

            default_region = st.selectbox(
                "Primary estimating region",
                profile_regions,
                index=region_index,
                help="Required. New projects start with this region."
            )

            preferred_supplier = st.text_input(
                "Primary supplier (optional)",
                value=profile.get("preferred_supplier", ""),
                placeholder="Example: ABC Ready Mix"
            )

            uploaded_avatar = st.file_uploader(
                "Upload profile avatar",
                type=["png", "jpg", "jpeg"]
            )

            save_company_profile = st.form_submit_button(
                "Save Company Profile"
            )

        if save_company_profile:
            if name.strip() and company.strip():
                save_profile(
                    name,
                    company,
                    phone,
                    email,
                    address,
                    default_region,
                    preferred_supplier
                )

                if preferred_supplier.strip():
                    pricing.add_supplier(preferred_supplier)

                if uploaded_avatar:
                    saved_avatar = save_avatar(
                        uploaded_avatar
                    )

                    if not saved_avatar:
                        st.error(
                            "Please upload a PNG or JPG image."
                        )
                        st.stop()

                st.success(
                    "Company profile saved successfully."
                )

            else:
                st.error(
                    "Your name and company name are required."
                )

with defaults_tab:
    st.subheader("Estimating Defaults")

    with st.expander(
            "Trade Waste Allowances",
            expanded=True
    ):
        st.caption(
            "Set your default waste allowances for new estimates."
        )

        with st.form("waste_allowance_form"):
            concrete_waste = st.number_input(
                "Concrete waste (%)",
                min_value=0.0,
                max_value=50.0,
                value=float(
                    preferences.get(
                        "concrete_waste_percent"
                    )
                ),
                step=0.5
            )

            lumber_waste = st.number_input(
                "Lumber waste (%)",
                min_value=0.0,
                max_value=50.0,
                value=float(
                    preferences.get(
                        "lumber_waste_percent"
                    )
                ),
                step=0.5
            )

            roofing_waste = st.number_input(
                "Roofing waste (%)",
                min_value=0.0,
                max_value=50.0,
                value=float(
                    preferences.get(
                        "roofing_waste_percent"
                    )
                ),
                step=0.5
            )

            drywall_waste = st.number_input(
                "Drywall waste (%)",
                min_value=0.0,
                max_value=50.0,
                value=float(
                    preferences.get(
                        "drywall_waste_percent"
                    )
                ),
                step=0.5
            )

            insulation_waste = st.number_input(
                "Insulation waste (%)",
                min_value=0.0,
                max_value=50.0,
                value=float(
                    preferences.get(
                        "insulation_waste_percent"
                    )
                ),
                step=0.5
            )

            save_waste_allowances = st.form_submit_button(
                "Save Waste Allowances"
            )

        if save_waste_allowances:
            preferences.update(
                {
                    "concrete_waste_percent": concrete_waste,
                    "lumber_waste_percent": lumber_waste,
                    "roofing_waste_percent": roofing_waste,
                    "drywall_waste_percent": drywall_waste,
                    "insulation_waste_percent": insulation_waste
                }
            )

            st.success("Waste allowances saved.")

    with st.expander(
            "Lumber and Framing Defaults",
            expanded=True
    ):
        st.caption(
            "Set company-wide defaults for standard framing estimates."
        )

        with st.form("lumber_defaults_form"):
            stud_spacing = st.number_input(
                "Default stud spacing (inches OC)",
                min_value=12.0,
                max_value=24.0,
                value=float(
                    preferences.get(
                        "lumber_stud_spacing_inches"
                    )
                ),
                step=0.5
            )

            stock_length = st.number_input(
                "Default lumber stock length (ft)",
                min_value=8.0,
                max_value=32.0,
                value=float(
                    preferences.get(
                        "lumber_stock_length_feet"
                    )
                ),
                step=1.0
            )

            save_lumber_defaults = st.form_submit_button(
                "Save Lumber Defaults"
            )

        if save_lumber_defaults:
            preferences.update(
                {
                    "lumber_stud_spacing_inches": stud_spacing,
                    "lumber_stock_length_feet": stock_length
                }
            )

            st.success("Lumber defaults saved.")

    with st.expander(
            "Concrete and Flatwork Defaults",
            expanded=True
    ):
        st.caption(
            "Set company defaults for base material and form products."
        )

        with st.form("concrete_defaults_form"):
            gravel_depth = st.number_input(
                "Default gravel base depth (inches)",
                min_value=1.0,
                max_value=12.0,
                value=float(
                    preferences.get(
                        "gravel_base_depth_inches"
                    )
                ),
                step=0.5
            )

            form_board_length = st.number_input(
                "Default form board length (ft)",
                min_value=4.0,
                max_value=32.0,
                value=float(
                    preferences.get(
                        "form_board_length_feet"
                    )
                ),
                step=1.0
            )

            form_tube_length = st.number_input(
                "Default concrete form tube length (ft)",
                min_value=2.0,
                max_value=12.0,
                value=float(
                    preferences.get(
                        "concrete_form_tube_length_feet"
                    )
                ),
                step=1.0
            )

            save_concrete_defaults = st.form_submit_button(
                "Save Concrete Defaults"
            )

        if save_concrete_defaults:
            preferences.update(
                {
                    "gravel_base_depth_inches": gravel_depth,
                    "form_board_length_feet": form_board_length,
                    "concrete_form_tube_length_feet": (
                        form_tube_length
                    )
                }
            )

            st.success("Concrete defaults saved.")

    st.caption(
        "Saved company defaults appear above. Additional reference "
        "values from Settings.py are shown below."
    )


    categories = {
        "Concrete and Structural": [
            "CONCRETE",
            "REBAR",
            "GRAVEL",
            "FORM"
        ],
        "Lumber and Framing": [
            "LUMBER",
            "STUD",
            "JOIST",
            "RAFTER",
            "BLOCKING",
            "COLLAR"
        ],
        "Roofing": [
            "ROOFING",
            "SHINGLE",
            "UNDERLAYMENT",
            "ICE",
            "DRIP",
            "RIDGE"
        ],
        "Drywall and Paint": [
            "DRYWALL",
            "CORNER",
            "JOINT",
            "TEXTURE",
            "PRIMER",
            "PAINT",
            "DOORS"
        ],
        "Insulation": [
            "INSULATION",
            "BATT",
            "BATTS",
            "BLOWN",
            "SPRAY_FOAM"
        ],
        "Plumbing and HVAC": [
            "PLUMBING",
            "HVAC"
        ]
    }

    used_settings = set()

    for category_name, keywords in categories.items():
        rows = []

        for setting_name, setting_value in all_settings.items():
            if any(
                keyword in setting_name
                for keyword in keywords
            ):
                rows.append(
                    {
                        "Setting": setting_name.replace(
                            "_",
                            " "
                        ).title(),
                        "Value": setting_value
                    }
                )

                used_settings.add(setting_name)

        if rows:
            with st.expander(
                    f"{category_name} ({len(rows)})",
                    expanded=False
            ):
                render_settings_table(rows)

    general_rows = []

    for setting_name, setting_value in all_settings.items():
        if setting_name not in used_settings:
            general_rows.append(
                {
                    "Setting": setting_name.replace(
                        "_",
                        " "
                    ).title(),
                    "Value": setting_value
                }
            )

    if general_rows:
        with st.expander(
                f"General ({len(general_rows)})",
                expanded=False
        ):
            render_settings_table(general_rows)

with pricing_tab:
    st.subheader("Regional Pricing")
    if open_pricing_setup:
        st.success(
            "Company defaults saved. Add your first supplier material "
            "price below, or return later from Settings."
        )
    st.caption(
        "Store supplier-specific material costs by market or delivery zone."
    )

    with st.expander("Supplier Directory", expanded=True):
        st.caption(
            "Add each supplier your company uses. Your primary supplier "
            "is selected in Company Profile."
        )

        with st.form("add_supplier_form"):
            new_supplier = st.text_input(
                "Supplier name",
                placeholder="Example: Home Depot or ABC Ready Mix"
            )

            add_supplier = st.form_submit_button("Add Supplier")

        if add_supplier:
            if pricing.add_supplier(new_supplier):
                st.success("Supplier added.")
            else:
                st.error("Enter a unique supplier name.")

        saved_suppliers = pricing.list_supplier_directory()

        if saved_suppliers:
            st.dataframe(
                [{"Supplier": supplier} for supplier in saved_suppliers],
                use_container_width=True,
                hide_index=True
            )

    region_names = pricing.list_regions()
    default_region = pricing.get_default_region()

    if region_names:
        default_index = 0

        if default_region in region_names:
            default_index = region_names.index(default_region)

        selected_default_region = st.selectbox(
            "Default pricing region for new projects",
            region_names,
            index=default_index,
            key="default_pricing_region"
        )

        if st.button("Save Default Pricing Region"):
            pricing.set_default_region(selected_default_region)
            st.success("Default pricing region saved.")

        st.divider()
        st.subheader("Material Prices")

        if "material_price_row_count" not in st.session_state:
            st.session_state.material_price_row_count = 1

        with st.form("material_price_form"):
            pricing_region = st.selectbox(
                "Pricing region",
                region_names,
                index=default_index,
                key="material_pricing_region"
            )

            material_supplier = st.text_input(
                "Supplier or store",
                value=profile.get("preferred_supplier", ""),
                placeholder=(
                    "Example: Home Depot Jonesboro #123 or "
                    "ABC Ready Mix"
                ),
                help=(
                    "Use the same supplier name on each material price. "
                    "It becomes a selectable project price list."
                )
            )

            material_price_date = st.date_input(
                "Price date",
                value=date.today()
            )

            st.caption("Material prices")
            material_entries = []

            for number in range(
                    st.session_state.material_price_row_count
            ):
                item_column, unit_column, cost_column = st.columns(3)

                with item_column:
                    material_item = st.text_input(
                        "Material item",
                        placeholder="Example: Ready Mix Concrete",
                        key=f"material_price_item_{number}"
                    )

                with unit_column:
                    material_unit = st.text_input(
                        "Unit",
                        placeholder="Example: CY",
                        key=f"material_price_unit_{number}"
                    )

                with cost_column:
                    material_unit_cost = st.number_input(
                        "Unit cost ($)",
                        min_value=0.0,
                        step=0.01,
                        key=f"material_price_cost_{number}"
                    )

                material_entries.append(
                    (
                        material_item,
                        material_unit,
                        material_unit_cost
                    )
                )

            add_material_row = st.form_submit_button(
                "+ Add Another Material"
            )
            save_material_prices = st.form_submit_button(
                "Save Material Prices"
            )

        if add_material_row:
            st.session_state.material_price_row_count += 1
            st.rerun()

        if save_material_prices:
            filled_entries = [
                entry
                for entry in material_entries
                if entry[0].strip() or entry[1].strip()
            ]
            incomplete_entry = any(
                not entry[0].strip() or not entry[1].strip()
                for entry in filled_entries
            )

            if (
                    filled_entries
                    and material_supplier.strip()
                    and not incomplete_entry
            ):
                for item, unit, unit_cost in filled_entries:
                    pricing.set_material_price(
                        item,
                        unit,
                        unit_cost,
                        pricing_region,
                        supplier=material_supplier,
                        price_date=material_price_date
                    )

                st.success(
                    f"Saved {len(filled_entries)} material price(s) for "
                    f"{pricing_region}."
                )
            else:
                st.error(
                    "Enter a supplier plus a material item and unit for "
                    "each material row."
                )

        with st.expander("AI Price Import (Review Required)"):
            st.caption(
                "Paste text from a supplier quote, receipt, cart, or product "
                "page. AI extracts possible unit prices, but nothing is saved "
                "until you review and confirm every row."
            )

            with st.form("ai_price_import_form"):
                ai_supplier = st.text_input(
                    "Supplier or store",
                    value=profile.get("preferred_supplier", ""),
                    key="ai_price_supplier"
                )

                ai_region = st.selectbox(
                    "Pricing region",
                    region_names,
                    index=default_index,
                    key="ai_price_region"
                )

                ai_price_date = st.date_input(
                    "Price date",
                    value=date.today(),
                    key="ai_price_date"
                )

                ai_source_text = st.text_area(
                    "Supplier quote, receipt, cart, or product-page text",
                    height=180,
                    placeholder=(
                        "Paste the copied material lines and prices here. "
                        "Do not paste credit-card, account, or customer data."
                    )
                )

                analyze_supplier_text = st.form_submit_button(
                    "Extract Price Candidates with AI"
                )

            if analyze_supplier_text:
                if not ai_supplier.strip() or not ai_source_text.strip():
                    st.error(
                        "Enter the supplier and paste supplier price text."
                    )
                else:
                    try:
                        candidates = EdenAI().extract_supplier_prices(
                            ai_source_text
                        )
                        st.session_state.ai_price_import = {
                            "supplier": ai_supplier.strip(),
                            "region": ai_region,
                            "price_date": ai_price_date,
                            "candidates": candidates
                        }
                        st.rerun()
                    except Exception as error:
                        st.error(
                            f"AI could not extract supplier prices: {error}"
                        )

            imported_prices = st.session_state.get(
                "ai_price_import"
            )

            if imported_prices is not None:
                candidates = imported_prices["candidates"]

                if not candidates:
                    st.warning(
                        "No reliable unit prices were found. Paste clearer "
                        "supplier material lines, then try again."
                    )
                else:
                    st.info(
                        "Review every material, unit, and cost before saving. "
                        "AI suggestions are not saved automatically."
                    )

                    with st.form("review_ai_price_import_form"):
                        reviewed_prices = []

                        for number, candidate in enumerate(candidates):
                            item_column, unit_column, cost_column = st.columns(3)

                            with item_column:
                                reviewed_item = st.text_input(
                                    "Material item",
                                    value=candidate["item"],
                                    key=f"review_ai_item_{number}"
                                )

                            with unit_column:
                                reviewed_unit = st.text_input(
                                    "Unit",
                                    value=candidate["unit"],
                                    key=f"review_ai_unit_{number}"
                                )

                            with cost_column:
                                reviewed_cost = st.number_input(
                                    "Unit cost ($)",
                                    min_value=0.0,
                                    value=float(candidate["unit_cost"]),
                                    step=0.01,
                                    key=f"review_ai_cost_{number}"
                                )

                            reviewed_prices.append(
                                (reviewed_item, reviewed_unit, reviewed_cost)
                            )

                        save_ai_import = st.form_submit_button(
                            "Save Reviewed Supplier Prices"
                        )

                    if save_ai_import:
                        incomplete_price = any(
                            not item.strip() or not unit.strip()
                            for item, unit, _ in reviewed_prices
                        )

                        if incomplete_price:
                            st.error(
                                "Every reviewed row needs a material item and unit."
                            )
                        else:
                            for item, unit, unit_cost in reviewed_prices:
                                pricing.set_material_price(
                                    item,
                                    unit,
                                    unit_cost,
                                    imported_prices["region"],
                                    supplier=imported_prices["supplier"],
                                    price_date=imported_prices["price_date"]
                                )

                            del st.session_state.ai_price_import
                            st.success(
                                f"Saved {len(reviewed_prices)} AI-reviewed "
                                "supplier price(s)."
                            )
                            st.rerun()

        selected_price_region = st.selectbox(
            "View price list for",
            region_names,
            index=default_index,
            key="view_pricing_region"
        )

        saved_prices = pricing.get_all_material_prices(
            selected_price_region
        )

        if saved_prices:
            price_rows = []

            for saved_price in saved_prices:
                price_rows.append(
                    {
                        "Item": saved_price["item"],
                        "Unit": saved_price["unit"],
                        "Unit Cost": (
                            f"${saved_price['unit_cost']:,.2f}"
                        ),
                        "Supplier / Store": saved_price.get(
                            "supplier",
                            "Not recorded"
                        ),
                        "Price Date": saved_price.get(
                            "price_date",
                            "Not recorded"
                        )
                    }
                )

            st.dataframe(
                price_rows,
                use_container_width=True,
                hide_index=True
            )

            with st.expander("Update a Saved Material Price"):
                st.caption(
                    "Save a newer unit cost instead of deleting the old one. "
                    "Eden keeps the previous price and date in price history."
                )
                price_choices = {
                    (
                        f"{saved_price['item']} · {saved_price['unit']} · "
                        f"{saved_price.get('supplier', 'Not recorded')}"
                    ): saved_price
                    for saved_price in saved_prices
                }
                selected_price_label = st.selectbox(
                    "Material price to update",
                    list(price_choices.keys())
                )
                selected_price = price_choices[selected_price_label]

                with st.form("update_saved_material_price_form"):
                    updated_unit_cost = st.number_input(
                        "New unit cost ($)",
                        min_value=0.0,
                        value=float(selected_price["unit_cost"]),
                        step=0.01
                    )
                    updated_price_date = st.date_input(
                        "Price date",
                        value=date.fromisoformat(
                            selected_price.get(
                                "price_date",
                                date.today().isoformat()
                            )
                        )
                        if selected_price.get("price_date", "").count("-") == 2
                        else date.today()
                    )
                    updated_supplier = st.text_input(
                        "Supplier / store",
                        value=selected_price.get(
                            "supplier",
                            "Not recorded"
                        )
                    )
                    save_price_update = st.form_submit_button(
                        "Save New Price"
                    )

                if save_price_update:
                    if updated_supplier.strip():
                        pricing.set_material_price(
                            selected_price["item"],
                            selected_price["unit"],
                            updated_unit_cost,
                            selected_price_region,
                            supplier=updated_supplier,
                            price_date=updated_price_date
                        )
                        st.success(
                            "New material price saved. The previous price "
                            "remains in its history."
                        )
                        st.rerun()
                    else:
                        st.error("Supplier or store is required.")

                price_history = pricing.get_material_price_history(
                    selected_price["item"],
                    selected_price["unit"],
                    selected_price_region,
                    selected_price.get("supplier", "Not recorded")
                )

                if price_history:
                    st.dataframe(
                        [
                            {
                                "Unit Cost": (
                                    f"${entry['unit_cost']:,.2f}"
                                ),
                                "Supplier": entry.get(
                                    "supplier",
                                    "Not recorded"
                                ),
                                "Price Date": entry.get(
                                    "price_date",
                                    "Not recorded"
                                ),
                                "Status": (
                                    "Current"
                                    if entry.get("current")
                                    else "Previous"
                                )
                            }
                            for entry in reversed(price_history)
                        ],
                        use_container_width=True,
                        hide_index=True
                    )
        else:
            st.info(
                "No material prices saved for this region yet."
            )
    else:
        st.info(
            "Create a pricing region before adding material prices."
        )
