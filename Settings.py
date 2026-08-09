class Settings:

    # =========================
    # GENERAL DEFAULTS
    # =========================

    # =========================
    # TRADE-SPECIFIC ALLOWANCES
    # =========================

    CONCRETE_WASTE_PERCENT = 10
    LUMBER_WASTE_PERCENT = 5
    ROOFING_WASTE_PERCENT = 10
    DRYWALL_WASTE_PERCENT = 10
    INSULATION_WASTE_PERCENT = 10
    DRYWALL_FINISH_WASTE_PERCENT = 10

    PLUMBING_LENGTH_ALLOWANCE_PERCENT = 10
    HVAC_LENGTH_ALLOWANCE_PERCENT = 10

    # Electrical devices, plumbing fixtures, and HVAC equipment are ordered
    # from approved schedules at exact quantities. No default waste is added.


    # =========================
    # STOCK MATERIAL LENGTHS
    # =========================

    LUMBER_STOCK_LENGTH_FEET = 20
    REBAR_STICK_LENGTH_FEET = 20
    DRIP_EDGE_PIECE_LENGTH_FEET = 10
    RIDGE_VENT_SECTION_LENGTH_FEET = 10
    CORNER_BEAD_PIECE_LENGTH_FEET = 8
    # =========================
    # LUMBER DEFAULT SPACING
    # =========================

    LUMBER_STUD_SPACING_INCHES = 16
    LUMBER_JOIST_SPACING_INCHES = 16
    LUMBER_RAFTER_SPACING_INCHES = 16
    LUMBER_BLOCKING_SPACING_INCHES = 16
    LUMBER_COLLAR_TIE_SPACING_INCHES = 48


    # =========================
    # SHEET MATERIAL COVERAGE
    # =========================

    DRYWALL_SHEET_COVERAGE_SQFT = 32      # 4 ft x 8 ft
    SHEATHING_SHEET_COVERAGE_SQFT = 32    # 4 ft x 8 ft


    # =========================
    # ROOFING COVERAGE
    # =========================

    ROOFING_SQUARE_COVERAGE_SQFT = 100
    SHINGLE_BUNDLES_PER_SQUARE = 3
    UNDERLAYMENT_ROLL_COVERAGE_SQFT = 1000
    ICE_WATER_SHIELD_ROLL_COVERAGE_SQFT = 200


    # =========================
    # INSULATION COVERAGE
    # =========================

    BATT_INSULATION_COVERAGE_PER_BATT_SQFT = 7.75
    BATTS_PER_BUNDLE = 8
    BLOWN_INSULATION_COVERAGE_PER_BAG_SQFT = 10.5
    SPRAY_FOAM_DEFAULT_COVERAGE_PER_KIT_SQFT = 200
    BATT_INSULATION_STUD_SPACING_INCHES = 16


    # =========================
    # DRYWALL FINISH COVERAGE
    # =========================

    JOINT_COMPOUND_COVERAGE_PER_BUCKET_SQFT = 450
    DRYWALL_TAPE_COVERAGE_PER_ROLL_SQFT = 500
    DRYWALL_SANDING_COVERAGE_PER_PACK_SQFT = 200
    DRYWALL_SCREWS_PER_SHEET = 32
    DRYWALL_SCREWS_PER_BOX = 1000


    # =========================
    # PAINT COVERAGE
    # =========================

    PRIMER_COVERAGE_PER_GALLON_SQFT = 400
    INTERIOR_PAINT_COVERAGE_PER_GALLON_SQFT = 350
    CEILING_PAINT_COVERAGE_PER_GALLON_SQFT = 350
    EXTERIOR_PAINT_COVERAGE_PER_GALLON_SQFT = 350
    TRIM_PAINT_COVERAGE_PER_GALLON_SQFT = 400
    DOORS_PER_GALLON = 2
    TEXTURE_COVERAGE_PER_BUCKET_SQFT = 300

    # =========================
    # CONCRETE TAKEOFF DEFAULTS
    # =========================

    WIRE_MESH_SHEET_COVERAGE_SQFT = 50   # 5 ft x 10 ft sheet
    VAPOR_BARRIER_ROLL_COVERAGE_SQFT = 2000
    GRAVEL_BASE_DEPTH_INCHES = 4
    FORM_BOARD_LENGTH_FEET = 16
    WALL_FORM_PANEL_COVERAGE_SQFT = 32
    FOUNDATION_WATERPROOFING_PAIL_COVERAGE_SQFT = 100
    CONCRETE_FORM_TUBE_LENGTH_FEET = 4
    FORM_PANEL_COVERAGE_SQFT = 32