from Lumber import LumberEstimator

from Roofing import RoofingEstimator

from Concrete import ConcreteEstimator

from Drywall import DrywallEstimator

from Insulation import InsulationEstimator

from DrywallFinish import DrywallFinishEstimator

from Electrical import ElectricalEstimator

from Plumbing import PlumbingEstimator

from HVAC import HVACEstimator

from Rebar import Rebar
from SpecialtyEstimates import SpecialtyEstimator

#### ESTIMATOR ####

class Estimator:

    def __init__(self):

        self.lumber=LumberEstimator()

        self.roofing=RoofingEstimator()

        self.concrete=ConcreteEstimator()

        self.drywall=DrywallEstimator()

        self.insulation=InsulationEstimator()

        self.drywall_finish=DrywallFinishEstimator()

        self.electrical=ElectricalEstimator()

        self.plumbing=PlumbingEstimator()

        self.hvac=HVACEstimator()

        self.rebar=Rebar()
        self.specialty=SpecialtyEstimator()

        self.name="Construction Estimator"

    def calculate_rebar(

                self,

                bar_size,

                linear_feet,

                waste_percent=10,

                stock_length_feet=20,

                source="approved_structural_plan"

        ):

            return self.rebar.calculate_rebar(

                bar_size=bar_size,

                linear_feet=linear_feet,

                waste_percent=waste_percent,

                stock_length_feet=stock_length_feet,

                source=source

            )

        ##################

        #### CONCRETE ####

        ##################

    def aggregate_base(
            self,
            area_sqft,
            depth_inches=None,
            material=None,
            tons_per_cubic_yard=None,
            purchase_unit=None,
            waste_percent=None
    ):
        return self.concrete.aggregate_base(
            area_sqft=area_sqft,
            depth_inches=depth_inches,
            material=material,
            tons_per_cubic_yard=tons_per_cubic_yard,
            purchase_unit=purchase_unit,
            waste_percent=waste_percent
        )

    def concrete_slab(

            self,

            length,

            width,

            thickness_inches,

            reinforced=False,

            rebar=None,

            wire_mesh=False,

            vapor_barrier=False,

            gravel_base=False,

            control_joints=False,

            forms=False,

            build_type=None,

            waste_percent=None

    ):

        return self.concrete.concrete_slab(

            length,

            width,

            thickness_inches,

            reinforced,

            rebar,

            wire_mesh,

            vapor_barrier,

            gravel_base,

            control_joints,

            forms,

            build_type,

            waste_percent

        )

    def concrete_footing(

            self,

            length,

            width,

            depth_inches,

            reinforced=False,

            rebar=None,

            forms=False,

            gravel_base=False,

            waste_percent=None,

            build_type = None

    ):

        return self.concrete.concrete_footing(

            length,

            width,

            depth_inches,

            reinforced,

            rebar,

            forms,

            gravel_base,

            waste_percent,

           build_type

        )

    def concrete_footing_system(
            self,
            footing_runs,
            reinforced=False,
            rebar=None,
            forms=False,
            gravel_base=False,
            waste_percent=None,
            build_type="Continuous Footing System"
    ):
        return self.concrete.concrete_footing_system(
            footing_runs,
            reinforced=reinforced,
            rebar=rebar,
            forms=forms,
            gravel_base=gravel_base,
            waste_percent=waste_percent,
            build_type=build_type
        )

    def concrete_foundation_wall(
            self,

            length,

            height,

            thickness_inches,

            reinforced=False,

            rebar=None,

            forms=False,

            waterproofing=False,

            build_type=None,

            waste_percent=None

    ):

        return self.concrete.concrete_foundation_wall(

            length,

            height,

            thickness_inches,

            reinforced,

            rebar,

            forms,

            waterproofing,

            build_type,

            waste_percent

        )

    def concrete_pad(

            self,

            length,

            width,

            thickness_inches,

            reinforced=False,

            rebar=None,

            wire_mesh=False,

            vapor_barrier=False,

            gravel_base=False,

            control_joints=False,

            forms=False,

            waste_percent=None

    ):

        return self.concrete.concrete_pad(

            length,

            width,

            thickness_inches,

            reinforced,

            rebar,

            wire_mesh,

            vapor_barrier,

            gravel_base,

            control_joints,

            forms,

            waste_percent

        )

    def concrete_pier(

            self,

            diameter_inches,

            height,

            quantity=1,

            reinforced=False,

            rebar=None,

            forms=False,

            gravel_base=False,

            waste_percent=None

    ):

        return self.concrete.concrete_pier(

            diameter_inches,

            height,

            quantity,

            reinforced,

            rebar,

            forms,

            gravel_base,

            waste_percent

        )

    def concrete_column(

            self,

            diameter_inches,

            height,

            quantity=1,

            reinforced=False,

            rebar=None,

            forms=False,

            waste_percent=None

    ):

        return self.concrete.concrete_column(

            diameter_inches,

            height,

            quantity,

            reinforced,

            rebar,

            forms,

            waste_percent

        )

    def concrete_curb(

            self,

            length,

            width_inches,

            height_inches,

            reinforced=False,

            rebar=None,

            forms=False,

            gravel_base=False,

            waste_percent=None

    ):

        return self.concrete.concrete_curb(

            length,

            width_inches,

            height_inches,

            reinforced,

            rebar,

            forms,

            gravel_base,

            waste_percent

        )

    def concrete_sidewalk(

            self,

            length,

            width,

            thickness_inches,

            reinforced=False,

            rebar=None,

            wire_mesh=False,

            vapor_barrier=False,

            gravel_base=False,

            control_joints=False,

            forms=False,

            waste_percent=None

    ):

        return self.concrete.concrete_sidewalk(

            length,

            width,

            thickness_inches,

            reinforced,

            rebar,

            wire_mesh,

            vapor_barrier,

            gravel_base,

            control_joints,

            forms,

            waste_percent

        )

    def concrete_driveway(

            self,

            length,

            width,

            thickness_inches,

            reinforced=False,

            rebar=None,

            wire_mesh=False,

            vapor_barrier=False,

            gravel_base=False,

            control_joints=False,

            forms=False,

            waste_percent=None

    ):

        return self.concrete.concrete_driveway(

            length,

            width,

            thickness_inches,

            reinforced,

            rebar,

            wire_mesh,

            vapor_barrier,

            gravel_base,

            control_joints,

            forms,

            waste_percent

        )

    def concrete_patio(

            self,

            length,

            width,

            thickness_inches,

            reinforced=False,

            rebar=None,

            wire_mesh=False,

            vapor_barrier=False,

            gravel_base=False,

            control_joints=False,

            forms=False,

            waste_percent=None

    ):

        return self.concrete.concrete_patio(

            length,

            width,

            thickness_inches,

            reinforced,

            rebar,

            wire_mesh,

            vapor_barrier,

            gravel_base,

            control_joints,

            forms,

            waste_percent

        )

    def concrete_steps(

            self,

            width,

            tread_depth,

            riser_height_inches,

            steps,

            reinforced=False,

            rebar=None,

            gravel_base=False,

            vapor_barrier=False,

            forms=False,

            waste_percent=None

    ):

        return self.concrete.concrete_steps(

            width,

            tread_depth,

            riser_height_inches,

            steps,

            reinforced,

            rebar,

            gravel_base,

            vapor_barrier,

            forms,

            waste_percent

        )

    def concrete_beam(

            self,

            length,

            width_inches,

            height_inches,

            reinforced=False,

            rebar=None,

            forms=False,

            waste_percent=None

    ):

        return self.concrete.concrete_beam(

            length,

            width_inches,

            height_inches,

            reinforced,

            rebar,

            forms,

            waste_percent

        )

    def concrete_ramp(

            self,

            length,

            width,

            height_inches,

            reinforced=False,

            rebar=None,

            gravel_base=False,

            forms=False,

            waste_percent=None

    ):

        return self.concrete.concrete_ramp(

            length,

            width,

            height_inches,

            reinforced,

            rebar,

            gravel_base,

            forms,

            waste_percent

        )

    def concrete_trench(
            self,
            length,
            width_inches,
            depth_inches,
            waste_percent=None
    ):

        return self.concrete.concrete_trench(

            length,

            width_inches,

            depth_inches,

            waste_percent=waste_percent

        )

    def concrete_retaining_wall(
            self,
            length,
            height,
            thickness_inches,
            waste_percent=None
    ):

        return self.concrete.concrete_retaining_wall(

            length,

            height,

            thickness_inches,

            waste_percent=waste_percent

        )

    def concrete_grade_beam(

            self,

            length,

            width_inches,

            height_inches,

            reinforced=False,

            rebar=None,

            forms=False,

            build_type=None,

            waste_percent=None

    ):

        return self.concrete.concrete_grade_beam(

            length,

            width_inches,

            height_inches,

            reinforced=reinforced,

            rebar=rebar,

            forms=forms,

            build_type=build_type,

            waste_percent=waste_percent

        )

    def concrete_spread_footing(
            self,
            length,
            width,
            depth_inches,
            waste_percent=None
    ):

        return self.concrete.concrete_spread_footing(

            length,

            width,

            depth_inches,

            waste_percent=waste_percent

        )

    def concrete_round_footing(
            self,
            diameter_inches,
            depth,
            quantity=1,
            waste_percent=None
    ):

        return self.concrete.concrete_round_footing(

            diameter_inches,

            depth,

            quantity,

            waste_percent=waste_percent

        )

    def concrete_pile_cap(
            self,
            length,
            width,
            depth_inches,
            waste_percent=None
    ):

        return self.concrete.concrete_pile_cap(

            length,

            width,

            depth_inches,

            waste_percent=waste_percent

        )

    def concrete_lintel(
            self,
            length,
            width_inches,
            height_inches,
            waste_percent=None
    ):

        return self.concrete.concrete_lintel(

            length,

            width_inches,

            height_inches,

            waste_percent=waste_percent

        )

    def concrete_slab_edge(

            self,

            length,

            width,

            edge_width_inches,

            edge_depth_inches,

            waste_percent=None

    ):

        return self.concrete.concrete_slab_edge(

            length,

            width,

            edge_width_inches,

            edge_depth_inches,

            waste_percent

        )

    ################

    #### LUMBER ####

    ################

    def frame_wall(

            self,

            length_feet,

            height_feet,

            stud_spacing_inches=None,

            quantity=1,

            waste_percent=None,

            plate_board_length=None

    ):

        return self.lumber.frame_wall(

            length_feet,

            height_feet,

            stud_spacing_inches=stud_spacing_inches,

            quantity=quantity,

            waste_percent=waste_percent,

            plate_board_length=plate_board_length

        )

    def frame_wall_with_openings(

            self,

            length_feet,

            height_feet,

            openings,

            stud_spacing_inches=None,

            quantity=1,

            waste_percent=None,

            plate_board_length=None,

            header_spec=None,

            header_plies=None

    ):

        return self.lumber.frame_wall_with_openings(

            length_feet=length_feet,

            height_feet=height_feet,

            openings=openings,

            stud_spacing_inches=stud_spacing_inches,

            quantity=quantity,

            waste_percent=waste_percent,

            plate_board_length=plate_board_length,

            header_spec=header_spec,

            header_plies=header_plies

        )

    def framing_hardware(self, hardware_items):
        return self.lumber.framing_hardware(hardware_items)

    def roof_trusses(
            self,
            building_length_feet,
            truss_spacing_inches=24,
            truss_spec="Roof Truss",
            connection_quantity=0
    ):
        return self.lumber.roof_trusses(
            building_length_feet,
            truss_spacing_inches=truss_spacing_inches,
            truss_spec=truss_spec,
            connection_quantity=connection_quantity
        )

    def wall_framing_package(
            self,
            length_feet,
            height_feet,
            quantity=1,
            stud_spacing_inches=None,
            include_sheathing=True,
            waste_percent=None
    ):
        return self.lumber.wall_framing_package(
            length_feet,
            height_feet,
            quantity=quantity,
            stud_spacing_inches=stud_spacing_inches,
            include_sheathing=include_sheathing,
            waste_percent=waste_percent
        )

    def stair_framing(
            self,
            stair_width_feet,
            tread_count,
            stringer_count,
            stringer_spec="2x12 Stair Stringer",
            tread_spec="Stair Tread",
            riser_spec="Stair Riser"
    ):
        return self.lumber.stair_framing(
            stair_width_feet,
            tread_count,
            stringer_count,
            stringer_spec=stringer_spec,
            tread_spec=tread_spec,
            riser_spec=riser_spec
        )

    def deck_framing(
            self,
            length_feet,
            projection_feet,
            joist_spacing_inches=16,
            post_count=0,
            joist_spec="2x8 Deck Joists",
            beam_spec="Plan-Specified Deck Beam"
    ):
        return self.lumber.deck_framing(
            length_feet,
            projection_feet,
            joist_spacing_inches=joist_spacing_inches,
            post_count=post_count,
            joist_spec=joist_spec,
            beam_spec=beam_spec
        )

    def garage_door_framing(
            self,
            opening_width_feet,
            wall_height_feet,
            quantity=1,
            header_spec=None,
            header_plies=None
    ):
        return self.lumber.garage_door_framing(
            opening_width_feet,
            wall_height_feet,
            quantity=quantity,
            header_spec=header_spec,
            header_plies=header_plies
        )

    def ceiling_joists(

            self,

            length,

            width,

            joist_spec=None,

            waste_percent=None

    ):

        return self.lumber.ceiling_joists(

            length,

            width,

            joist_spec=joist_spec,

            waste_percent=waste_percent

        )

    def rafters(

            self,

            span,

            roof_length,

            pitch,

            rafter_spec=None

    ):

        return self.lumber.rafters(

            span,

            roof_length,

            pitch,

            rafter_spec=rafter_spec

        )

    def ridge_board(self,

                    length,

                    ridge_spec=None,

                    waste_percent = None

                    ):

        return self.lumber.ridge_board(

            length,

            ridge_spec=ridge_spec,

            waste_percent = waste_percent

        )

    def collar_ties(self, length, tie_spec=None, waste_percent=None):

        return self.lumber.collar_ties(

            length,

            tie_spec=tie_spec

        )

    def roof_sheathing(
            self,
            length,
            width,
            roof_type="gable",
            pitch_rise=6.0,
            overhang_inches=12.0,
            waste_percent=None
    ):
        return self.lumber.roof_sheathing(
            length,
            width,
            roof_type=roof_type,
            pitch_rise=pitch_rise,
            overhang_inches=overhang_inches,
            waste_percent=waste_percent
        )

    def wall_sheathing(self, length, height, waste_percent=None):

        return self.lumber.wall_sheathing(

            length,

            height,

            waste_percent=waste_percent

        )

    def headers(self, opening_width, header_spec=None, waste_percent=None):

        return self.lumber.headers(

            opening_width,

            header_spec=header_spec,

            waste_percent=waste_percent

        )

    def blocking(

            self,

            length,

            stud_spacing_inches=None,

            rows=1,

            waste_percent=None

    ):

        return self.lumber.blocking(

            length,

            stud_spacing_inches=stud_spacing_inches,

            rows=rows,

            waste_percent=waste_percent

        )

    def subfloor_sheathing(self, length, width, waste_percent=None):

        return self.lumber.subfloor_sheathing(

            length,

            width,

            waste_percent=waste_percent

        )

    def rim_joists(self, length, width, rim_spec=None, waste_percent=None):

        return self.lumber.rim_joists(

            length,

            width,

            rim_spec=rim_spec,

            waste_percent=waste_percent

        )

    def shingles(
            self,
            length,
            width,
            roof_type="gable",
            pitch_rise=6.0,
            overhang_inches=12.0,
            waste_percent=None
    ):
        return self.roofing.shingles(
            length,
            width,
            roof_type=roof_type,
            pitch_rise=pitch_rise,
            overhang_inches=overhang_inches,
            waste_percent=waste_percent
        )

    def underlayment(
            self,
            length_feet,
            width_feet,
            roof_type="gable",
            pitch_rise=6.0,
            overhang_inches=12.0,
            waste_percent=None
    ):
        return self.roofing.underlayment(
            length_feet,
            width_feet,
            roof_type=roof_type,
            pitch_rise=pitch_rise,
            overhang_inches=overhang_inches,
            waste_percent=waste_percent
        )

    def drip_edge(self, required_length_feet, waste_percent=None):

        return self.roofing.drip_edge(

            required_length_feet,

            waste_percent=waste_percent

        )

    def ice_water_shield(self, required_coverage_sqft, waste_percent=None):

        return self.roofing.ice_water_shield(

            required_coverage_sqft,

            waste_percent=waste_percent

        )

    def ridge_vent(self, length_feet, waste_percent=None):

        return self.roofing.ridge_vent(

            length_feet,

            waste_percent=waste_percent

        )

    def flashing(self, quantity, waste_percent=None):

        return self.roofing.flashing(

            quantity,

            waste_percent=waste_percent

        )

    def studs(

            self,

            wall_length,

            wall_height,

            stud_spacing_inches=None,

            waste_percent=None

    ):

        return self.lumber.studs(

            wall_length,

            wall_height,

            stud_spacing_inches=stud_spacing_inches,

            waste_percent=waste_percent

        )

    def king_studs(self,openings,wall_height, waste_percent=None):

        return self.lumber.king_studs(

            openings,

            wall_height,

            waste_percent=waste_percent

        )

    def jack_studs(self,openings,opening_height,waste_percent=None):

        return self.lumber.jack_studs(

            openings,

            opening_height,

            waste_percent=waste_percent

        )

    def cripple_studs(self,openings,opening_width,stud_spacing_inches=16, waste_percent=None):

        return self.lumber.cripple_studs(

            openings,

            opening_width,

            stud_spacing_inches,

            waste_percent=waste_percent

        )

    def corner_posts(self,corners,wall_height, waste_percent=None):

        return self.lumber.corner_posts(

            corners,

            wall_height,

            waste_percent=waste_percent

        )

    def plates(

            self,

            length,

            plate_type="double top",

            waste_percent=None,

            stock_length_feet=None

    ):

        return self.lumber.plates(

            length,

            plate_type=plate_type,

            waste_percent=waste_percent,

            stock_length_feet=stock_length_feet

        )

    def sill_plate(self,length, waste_percent=None):

        return self.lumber.sill_plate(

            length,

            waste_percent=waste_percent

        )

    def posts(self, quantity, height, post_spec=None, waste_percent=None):

        return self.lumber.posts(

            quantity,

            height,

            post_spec=post_spec,

            waste_percent=waste_percent

        )

    def beams(self, length, beam_spec=None, waste_percent=None):

        return self.lumber.beams(

            length,

            beam_spec=beam_spec,

            waste_percent=waste_percent

        )

    #################

    #### DRYWALL ####

    #################

    def wall_drywall(

            self,

            length,

            height,

            quantity=1,

            waste_percent=None

    ):

        return self.drywall.wall_drywall(

            length,

            height,

            quantity=quantity,

            waste_percent=waste_percent

        )

    def ceiling_drywall(

            self,

            length,

            width,

            waste_percent=None

    ):

        return self.drywall.ceiling_drywall(

            length,

            width,

            waste_percent=waste_percent

        )

    ####################

    #### INSULATION ####

    ####################

    def batt_insulation(

            self,

            length,

            height,

            r_value="R-13",

            stud_spacing=16,

            quantity=1,

            waste_percent = None

    ):

        return self.insulation.batt_insulation(

            length,

            height,

            r_value=r_value,

            stud_spacing=stud_spacing,

            quantity=quantity,

            waste_percent=waste_percent

        )

    def blown_insulation(

            self,

            length,

            width,

            r_value="R-38",

            waste_percent=None

    ):

        return self.insulation.blown_insulation(

            length,

            width,

            r_value=r_value,

            waste_percent=waste_percent

        )

    def spray_foam(

            self,

            length,

            height,

            thickness_inches,

            coverage_per_kit_sqft,

            waste_percent=None

    ):

        return self.insulation.spray_foam(

            length,

            height,

            thickness_inches=thickness_inches,

            coverage_per_kit_sqft=coverage_per_kit_sqft,

            waste_percent=waste_percent

        )

    ########################

    #### DRYWALL FINISH ####

    ########################

    def joint_compound(self, area):

        return self.drywall_finish.joint_compound(

            area

        )

    def drywall_tape(self, area):

        return self.drywall_finish.drywall_tape(

            area

        )

    def corner_bead(self, length):

        return self.drywall_finish.corner_bead(

            length

        )

    def drywall_screws(self, area):

        return self.drywall_finish.drywall_screws(

            area

        )

    def drywall_sanding(self, area):

        return self.drywall_finish.drywall_sanding(

            area

        )

    def drywall_primer(self, area):

        return self.drywall_finish.primer(

            area

        )

    def drywall_texture(self, area):

        return self.drywall_finish.texture(

            area

        )

    def interior_paint(self, area):

        return self.drywall_finish.interior_paint(

            area

        )

    def ceiling_paint(self, area):

        return self.drywall_finish.ceiling_paint(

            area

        )

    def trim_paint(self, length, face_width_inches):

        return self.drywall_finish.trim_paint(

            length,

            face_width_inches

        )

    def door_paint(self, quantity):

        return self.drywall_finish.door_paint(

            quantity

        )

    def exterior_paint(self, area):

        return self.drywall_finish.exterior_paint(

            area

        )

    ####################

    #### ELECTRICAL ####

    ####################

    def electrical_outlets(self, quantity, outlet_spec=None):

        return self.electrical.outlets(

            quantity,

            outlet_spec=outlet_spec

        )

    def electrical_switches(self, quantity, switch_spec=None):

        return self.electrical.switches(

            quantity,

            switch_spec=switch_spec

        )

    def electrical_lighting_fixtures(self, quantity, fixture_spec=None):

        return self.electrical.lighting_fixtures(

            quantity,

            fixture_spec=fixture_spec

        )

    def electrical_boxes(self, quantity, box_spec=None):

        return self.electrical.electrical_boxes(

            quantity,

            box_spec=box_spec

        )

    def electrical_romex(self, length, wire_type=None):

        return self.electrical.romex(

            length,

            wire_type=wire_type

        )

    def electrical_breakers(self, quantity, breaker_spec=None):

        return self.electrical.breakers(

            quantity,

            breaker_spec=breaker_spec

        )

    def electrical_panel(self, panel_spec=None):

        return self.electrical.electrical_panel(

            panel_spec=panel_spec

        )

    ##################

    #### PLUMBING ####

    ##################

    def pex_pipe(self, length, pipe_spec=None):

        return self.plumbing.pex_pipe(

            length,

            pipe_spec=pipe_spec

        )

    def pvc_drain_pipe(self, length, pipe_spec=None):

        return self.plumbing.pvc_drain_pipe(

            length,

            pipe_spec=pipe_spec

        )

    def copper_pipe(self, length, pipe_spec=None):

        return self.plumbing.copper_pipe(

            length,

            pipe_spec=pipe_spec

        )

    def plumbing_fittings(self, quantity, fitting_spec=None):

        return self.plumbing.fittings(

            quantity,

            fitting_spec=fitting_spec

        )

    def plumbing_valve(self, quantity, valve_spec=None):

        return self.plumbing.plumbing_valve(

            quantity,

            valve_spec=valve_spec

        )

    def toilets(self, quantity, fixture_spec=None):

        return self.plumbing.toilets(

            quantity,

            fixture_spec=fixture_spec

        )

    def sink(self, quantity, fixture_spec=None):

        return self.plumbing.sink(

            quantity,

            fixture_spec=fixture_spec

        )

    def faucet(self, quantity, fixture_spec=None):

        return self.plumbing.faucet(

            quantity,

            fixture_spec=fixture_spec

        )

    def showers_tubs(self, quantity, fixture_spec=None):

        return self.plumbing.showers_tubs(

            quantity,

            fixture_spec=fixture_spec

        )

    def water_heater(self, quantity, heater_spec=None):

        return self.plumbing.water_heater(

            quantity,

            heater_spec=heater_spec

        )

    ##############

    #### HVAC ####

    ##############

    def ductwork(self, length, duct_spec=None):

        return self.hvac.ductwork(

            length,

            duct_spec=duct_spec

        )

    def supply_register(self, quantity, register_spec=None):

        return self.hvac.supply_register(

            quantity,

            register_spec=register_spec

        )

    def return_grilles(self, quantity, grille_spec=None):

        return self.hvac.return_grilles(

            quantity,

            grille_spec=grille_spec

        )

    def flex_duct(self, length, duct_spec=None):

        return self.hvac.flex_duct(

            length,

            duct_spec=duct_spec

        )

    def thermostat(self, quantity, thermostat_spec=None):

        return self.hvac.thermostat(

            quantity,

            thermostat_spec=thermostat_spec

        )

    def air_filters(self, quantity, filter_spec=None):

        return self.hvac.air_filters(

            quantity,

            filter_spec=filter_spec

        )

    def refrigerant_line_set(self, length, line_set_spec=None):

        return self.hvac.refrigerant_line_set(

            length,

            line_set_spec=line_set_spec

        )

    def condensate_drain(self, length, drain_spec=None):

        return self.hvac.condensate_drain(

            length,

            drain_spec=drain_spec

        )

    def furnace(self, quantity, furnace_spec=None):

        return self.hvac.furnace(

            quantity,

            furnace_spec=furnace_spec

        )

    def air_conditioner(self, quantity, ac_spec=None):

        return self.hvac.air_conditioner(

            quantity,

            ac_spec=ac_spec

        )

    ###############

    #### REBAR ####

    ###############

    def rebar(self,bar_size,linear_feet,waste_percent=10

    ):

        return self.rebar.calculate_rebar(

            bar_size,

            linear_feet,

            waste_percent

        )

    def concrete_custom_flatwork(
            self,

            area_sqft,

            perimeter_lf,

            thickness_inches,

            reinforced=False,

            rebar=None,

            wire_mesh=False,

            vapor_barrier=False,

            gravel_base=False,

            control_joints=False,

            forms=False,

            build_type="Custom Concrete Flatwork",

            waste_percent=None

    ):

        return self.concrete.concrete_custom_flatwork(
            area_sqft=area_sqft,

            perimeter_lf=perimeter_lf,

            thickness_inches=thickness_inches,

            reinforced=reinforced,

            rebar=rebar,

            wire_mesh=wire_mesh,

            vapor_barrier=vapor_barrier,

            gravel_base=gravel_base,

            control_joints=control_joints,

            forms=forms,

            build_type=build_type,

            waste_percent=waste_percent
        )

    ##########################
    #### PROJECT ASSEMBLIES ####
    ##########################

    @staticmethod
    def _combine_material_takeoffs(*takeoffs):
        """Combine matching material rows from several Eden estimates."""
        totals = {}

        for takeoff in takeoffs:
            for item in takeoff:
                name = item.get("item")
                unit = item.get("unit")
                quantity = item.get("quantity")

                if not name or not unit or quantity is None:
                    continue

                key = (name, unit)
                totals[key] = totals.get(key, 0) + quantity

        combined = []

        for (name, unit), quantity in sorted(totals.items()):
            if isinstance(quantity, float):
                quantity = round(quantity, 2)

                if quantity.is_integer():
                    quantity = int(quantity)

            combined.append(
                {
                    "item": name,
                    "unit": unit,
                    "quantity": quantity
                }
            )

        return combined

    def residential_house_takeoff(
            self,
            house_name,
            components,
            story_count=1
    ):
        """Combine separately measured residential assemblies into one bid review.

        This method deliberately receives completed assemblies instead of
        inventing structural or architectural details.  That keeps a whole
        house takeoff traceable back to the plan-confirmed component that
        produced every material row.
        """
        if not components:
            raise ValueError(
                "Add at least one measured house component before combining "
                "a whole-house takeoff."
            )

        normalized_takeoffs = []

        for component in components.values():
            normalized_rows = []

            for item in component["material_takeoff"]:
                normalized_item = item.copy()
                normalized_item["item"] = (
                    normalized_item["item"]
                    .replace(
                        " Wall, King, and Jack Studs",
                        " Studs"
                    )
                    .replace(
                        " Top and Bottom Plates",
                        " Plates"
                    )
                )
                normalized_rows.append(normalized_item)

            normalized_takeoffs.append(normalized_rows)

        material_takeoff = self._combine_material_takeoffs(
            *normalized_takeoffs
        )

        return {
            "type": "Residential Whole-House Takeoff",
            "house_name": house_name,
            "story_count": story_count,
            "component_estimates": components,
            "component_count": len(components),
            "material_takeoff": material_takeoff,
            "assumptions": [
                "Each component uses plan-confirmed measurements entered "
                "during this takeoff.",
                "Matching material rows are combined for a project-level "
                "ordering summary.",
                "Components remain separate in the saved estimate for "
                "trade-by-trade review."
            ],
            "exclusions": [
                "Structural member selection, engineering, and connections "
                "unless specifically provided from approved plans",
                "Sitework, excavation, utilities, permits, inspections, "
                "labor, equipment, and subcontractor scope unless separately estimated",
                "Unentered rooms, wall groups, roof planes, openings, and "
                "finish selections"
            ],
            "scope_note": (
                "Review every component against the approved plan set before "
                "ordering or issuing a customer proposal. This is a combined "
                "material takeoff, not a structural design or permit estimate."
            )
        }

    def backyard_studio_shell(
            self,
            length,
            width,
            wall_height,
            slab_thickness_inches=4,
            include_interior_finish=False,
            insulation_r_value="R-13"
    ):
        """Build a starter material takeoff for a simple rectangular studio.

        This assembly intentionally excludes openings, structural header
        design, foundation design, electrical, plumbing, HVAC, siding, and
        permits. Those items require project-specific selections or plans.
        """
        slab = self.concrete_slab(
            length,
            width,
            slab_thickness_inches,
            wire_mesh=True,
            vapor_barrier=True,
            gravel_base=True,
            control_joints=True,
            forms=True,
            build_type="Studio Shell Slab Package"
        )

        long_walls = self.frame_wall(
            length,
            wall_height,
            quantity=2
        )
        short_walls = self.frame_wall(
            width,
            wall_height,
            quantity=2
        )

        long_wall_sheathing = self.wall_sheathing(
            length,
            wall_height * 2
        )
        short_wall_sheathing = self.wall_sheathing(
            width,
            wall_height * 2
        )
        roof_sheathing = self.roof_sheathing(length, width)
        shingles = self.shingles(length, width)

        component_estimates = {
            "Slab package": slab,
            "Wall framing": long_walls,
            "Wall framing (end walls)": short_walls,
            "Wall sheathing": long_wall_sheathing,
            "Wall sheathing (end walls)": short_wall_sheathing,
            "Roof sheathing": roof_sheathing,
            "Roof shingles": shingles
        }

        if include_interior_finish:
            long_wall_insulation = self.batt_insulation(
                length,
                wall_height,
                r_value=insulation_r_value,
                quantity=2
            )
            short_wall_insulation = self.batt_insulation(
                width,
                wall_height,
                r_value=insulation_r_value,
                quantity=2
            )
            long_wall_drywall = self.wall_drywall(
                length,
                wall_height,
                quantity=2
            )
            short_wall_drywall = self.wall_drywall(
                width,
                wall_height,
                quantity=2
            )
            ceiling_drywall = self.ceiling_drywall(length, width)
            wall_area = 2 * (length + width) * wall_height
            paint = self.interior_paint(wall_area)

            component_estimates.update(
                {
                    "Wall insulation": long_wall_insulation,
                    "Wall insulation (end walls)": short_wall_insulation,
                    "Wall drywall": long_wall_drywall,
                    "Wall drywall (end walls)": short_wall_drywall,
                    "Ceiling drywall": ceiling_drywall,
                    "Interior wall paint": paint
                }
            )

        material_takeoff = self._combine_material_takeoffs(
            *[
                estimate["material_takeoff"]
                for estimate in component_estimates.values()
            ]
        )

        return {
            "type": "Backyard Studio Shell",
            "dimensions": {
                "length": length,
                "width": width,
                "wall_height": wall_height
            },
            "slab_thickness_inches": slab_thickness_inches,
            "include_interior_finish": include_interior_finish,
            "insulation_r_value": (
                insulation_r_value
                if include_interior_finish
                else None
            ),
            "component_estimates": component_estimates,
            "material_takeoff": material_takeoff,
            "scope_note": (
                "Starter shell only. Verify all measurements, roof design, "
                "structural requirements, openings, and local code before "
                "ordering materials."
            ),
            "exclusions": [
                "Doors and windows",
                "Headers and engineered structural items",
                "Siding, trim, and exterior weatherproofing",
                "Electrical, plumbing, HVAC, permits, and labor"
            ]
        }

    def exterior_wall_assembly(
            self,
            length_feet,
            height_feet,
            quantity=1,
            stud_spacing_inches=None,
            include_housewrap=True,
            include_insulation=False,
            include_drywall=False,
            insulation_r_value="R-13",
            openings=None,
            header_spec=None,
            header_plies=None,
            waste_percent=None
    ):
        """Create a traceable starter assembly for repeated exterior walls.

        This is deliberately a measured wall *segment* assembly. It does not
        invent structural or opening details from a generic wall size.
        """
        gross_wall_area = length_feet * height_feet * quantity
        openings = openings or []

        opening_area_per_wall = sum(
            opening["width_feet"] * opening["height_feet"]
            for opening in openings
        )

        if opening_area_per_wall >= length_feet * height_feet:
            raise ValueError(
                "Openings cannot equal or exceed the area of one wall."
            )

        if openings:
            framing = self.frame_wall_with_openings(
                length_feet=length_feet,
                height_feet=height_feet,
                openings=openings,
                quantity=quantity,
                stud_spacing_inches=stud_spacing_inches,
                waste_percent=waste_percent,
                header_spec=header_spec,
                header_plies=header_plies
            )
            net_wall_area = framing["net_wall_area_sqft"]
            components = {
                "Wall and opening framing": framing,
                "Wall sheathing": self.lumber.wall_sheathing_area(
                    net_wall_area,
                    waste_percent=framing["waste_percent"]
                )
            }
        else:
            framing = self.wall_framing_package(
                length_feet=length_feet,
                height_feet=height_feet,
                quantity=quantity,
                stud_spacing_inches=stud_spacing_inches,
                include_sheathing=True,
                waste_percent=waste_percent
            )
            net_wall_area = gross_wall_area
            components = {
                "Wall framing and sheathing": framing
            }

        if include_housewrap:
            components["Housewrap"] = self.housewrap(
                net_wall_area,
                waste_percent=framing["waste_percent"]
            )

        if include_insulation:
            components["Wall insulation"] = self.insulation.batt_insulation_area(
                net_wall_area,
                r_value=insulation_r_value,
                waste_percent=framing["waste_percent"]
            )

        if include_drywall:
            components["Interior wall drywall"] = self.drywall.wall_drywall_area(
                net_wall_area,
                waste_percent=framing["waste_percent"]
            )

        return {
            "type": "Exterior Wall Assembly",
            "dimensions": {
                "length": length_feet,
                "height": height_feet
            },
            "quantity": quantity,
            "gross_wall_area_sqft": round(gross_wall_area, 2),
            "net_wall_area_sqft": round(net_wall_area, 2),
            "stud_spacing_inches": (
                f"{framing['stud_spacing_inches']} in OC"
                if openings else
                framing["details"]["Stud spacing"]
            ),
            "openings": openings,
            "header_spec": (
                framing.get("header_spec") if openings else None
            ),
            "header_plies": (
                framing.get("header_plies") if openings else None
            ),
            "include_housewrap": include_housewrap,
            "include_insulation": include_insulation,
            "include_drywall": include_drywall,
            "insulation_r_value": (
                insulation_r_value if include_insulation else None
            ),
            "waste_percent": framing["waste_percent"],
            "component_estimates": components,
            "material_takeoff": self._combine_material_takeoffs(
                *[
                    component["material_takeoff"]
                    for component in components.values()
                ]
            ),
            "assumptions": [
                "Straight, repeated wall segments with 2x4 framing.",
                "Wall sheathing is included.",
                (
                    "Covering materials use net wall area after repeated "
                    "openings are deducted."
                    if openings else
                    "Wall area is gross area because no openings were entered."
                )
            ],
            "exclusions": [
                (
                    "Door and window units, flashing, and installation "
                    "accessories"
                    if openings else
                    "Doors, windows, headers, and opening framing"
                ),
                "Engineered design, hold-downs, and structural hardware",
                "Flashing tape, siding, trim, fasteners, and sealants",
                "Electrical, plumbing, labor, permits, and local code review"
            ],
            "scope_note": (
                "For this assembly, every identical wall segment uses the "
                "same opening layout. Estimate non-repeating walls "
                "separately and review structural details against approved "
                "plans."
            )
        }

    def foundation_system_assembly(
            self,
            footing_runs,
            reinforced=True,
            forms=True,
            gravel_base=False,
            include_foundation_wall=False,
            foundation_wall_length_feet=None,
            foundation_wall_height_feet=None,
            foundation_wall_thickness_inches=8,
            include_waterproofing=False,
            waste_percent=None
    ):
        """Create a traceable residential footing and wall foundation scope.

        Footing runs are measured independently. Foundation-wall length is
        requested separately because interior footings and stem walls often
        do not share the same total length.
        """
        plan_required_rebar = (
            {
                "status": "plan_required",
                "source": "approved_structural_plan",
                "schedule": None
            }
            if reinforced else None
        )
        footing_system = self.concrete_footing_system(
            footing_runs,
            reinforced=reinforced,
            rebar=plan_required_rebar,
            forms=forms,
            gravel_base=gravel_base,
            waste_percent=waste_percent,
            build_type="Residential Foundation Footing Package"
        )
        components = {
            "Continuous footing system": footing_system
        }

        if include_foundation_wall:
            if (
                    not foundation_wall_length_feet or
                    not foundation_wall_height_feet
            ):
                raise ValueError(
                    "Foundation-wall length and height are required."
                )

            components["Foundation wall"] = self.concrete_foundation_wall(
                foundation_wall_length_feet,
                foundation_wall_height_feet,
                foundation_wall_thickness_inches,
                reinforced=reinforced,
                rebar=plan_required_rebar,
                forms=forms,
                waterproofing=include_waterproofing,
                build_type="Residential Foundation Wall Package",
                waste_percent=footing_system["waste_percent"]
            )

        foundation_wall_estimate = components.get("Foundation wall")

        return {
            "type": "Residential Foundation System Assembly",
            "footing_runs": footing_system["footing_runs"],
            "footing_run_count": footing_system["run_count"],
            "footing_cubic_yards": footing_system["cubic_yards"],
            "footing_order_quantity": footing_system["order_quantity"],
            "include_foundation_wall": include_foundation_wall,
            "foundation_wall": (
                {
                    "length": foundation_wall_length_feet,
                    "height": foundation_wall_height_feet,
                    "thickness_inches": foundation_wall_thickness_inches,
                    "waterproofing": include_waterproofing
                }
                if include_foundation_wall else None
            ),
            "foundation_wall_cubic_yards": (
                foundation_wall_estimate["cubic_yards"]
                if foundation_wall_estimate else None
            ),
            "foundation_wall_order_quantity": (
                foundation_wall_estimate["order_quantity"]
                if foundation_wall_estimate else None
            ),
            "reinforced": reinforced,
            "forms": forms,
            "gravel_base": gravel_base,
            "waste_percent": footing_system["waste_percent"],
            "component_estimates": components,
            "material_takeoff": self._combine_material_takeoffs(
                *[
                    component["material_takeoff"]
                    for component in components.values()
                ]
            ),
            "assumptions": [
                "Footing runs are measured continuous runs before waste.",
                "Footing concrete is rounded once for the entire footing system.",
                (
                    "Foundation-wall concrete is a separate pour and is "
                    "shown as a separate component."
                    if include_foundation_wall else
                    "Foundation walls are not included."
                )
            ],
            "exclusions": [
                "Excavation, haul-off, dewatering, soil correction, and backfill",
                "Drain tile, stone, sump equipment, and drainage design",
                "Rebar quantities, engineering, stepped elevations, and bearing design",
                "Labor, permits, inspections, and local code review"
            ],
            "scope_note": (
                "Footing sizes, reinforcing, elevations, foundation-wall "
                "layout, waterproofing system, and site drainage must match "
                "approved plans and site conditions. Footing and wall "
                "concrete are separate pours; do not treat their combined "
                "takeoff total as one truck order."
            )
        }

    def roof_covering_assembly(
            self,
            length_feet,
            width_feet,
            roof_type="gable",
            pitch_rise=6.0,
            overhang_inches=12.0,
            include_drip_edge=True,
            include_ridge_vent=True,
            ice_water_coverage_sqft=0,
            flashing_quantity=0,
            waste_percent=None
    ):
        """Create a measured roof-covering assembly, not roof framing."""
        roof_waste_percent = self.roofing._get_roofing_waste_percent(
            waste_percent
        )
        sheathing = self.roof_sheathing(
            length_feet,
            width_feet,
            roof_type=roof_type,
            pitch_rise=pitch_rise,
            overhang_inches=overhang_inches,
            waste_percent=roof_waste_percent
        )
        shingles = self.shingles(
            length_feet,
            width_feet,
            roof_type=roof_type,
            pitch_rise=pitch_rise,
            overhang_inches=overhang_inches,
            waste_percent=roof_waste_percent
        )
        underlayment = self.underlayment(
            length_feet,
            width_feet,
            roof_type=roof_type,
            pitch_rise=pitch_rise,
            overhang_inches=overhang_inches,
            waste_percent=roof_waste_percent
        )
        components = {
            "Roof sheathing": sheathing,
            "Roof shingles": shingles,
            "Roof underlayment": underlayment
        }
        roof_length = sheathing["roof_length"]
        rafter_length = sheathing["rafter_length"]
        roof_type = sheathing["roof_type"]

        drip_edge_length = (
            2 * roof_length + 4 * rafter_length
            if roof_type == "gable" else
            2 * roof_length + 2 * rafter_length
        )

        if include_drip_edge:
            components["Drip edge"] = self.drip_edge(
                drip_edge_length,
                waste_percent=shingles["waste_percent"]
            )

        if include_ridge_vent and roof_type == "gable":
            components["Ridge vent"] = self.ridge_vent(
                roof_length,
                waste_percent=shingles["waste_percent"]
            )

        if ice_water_coverage_sqft > 0:
            components["Ice and water shield"] = self.ice_water_shield(
                ice_water_coverage_sqft,
                waste_percent=shingles["waste_percent"]
            )

        if flashing_quantity > 0:
            components["Roof flashing"] = self.flashing(
                flashing_quantity,
                waste_percent=shingles["waste_percent"]
            )

        return {
            "type": "Residential Roof Covering Assembly",
            "dimensions": {
                "length": length_feet,
                "width": width_feet
            },
            "roof_type": roof_type,
            "pitch_rise": sheathing["pitch_rise"],
            "overhang_inches": sheathing["overhang_inches"],
            "roof_area_sqft": sheathing["area"],
            "roof_length_feet": roof_length,
            "rafter_length_feet": rafter_length,
            "drip_edge_length_feet": round(drip_edge_length, 2),
            "include_drip_edge": include_drip_edge,
            "include_ridge_vent": include_ridge_vent and roof_type == "gable",
            "ice_water_coverage_sqft": ice_water_coverage_sqft,
            "flashing_quantity": flashing_quantity,
            "waste_percent": shingles["waste_percent"],
            "component_estimates": components,
            "material_takeoff": self._combine_material_takeoffs(
                *[
                    component["material_takeoff"]
                    for component in components.values()
                ]
            ),
            "assumptions": [
                "Roof coverage uses the entered pitch and overhangs.",
                "Drip edge follows the calculated roof perimeter.",
                "Ice-and-water coverage is measured from plans or local requirements."
            ],
            "exclusions": [
                "Trusses, rafters, blocking, framing connections, and structural design",
                "Valleys, hips, dormers, skylights, penetrations, and complex flashing unless entered",
                "Roof removal, decking repairs, labor, permits, and local code review"
            ],
            "scope_note": (
                "This is a roof-covering assembly for simple gable or shed "
                "geometry. Verify roof planes, valleys, penetrations, "
                "ventilation, and manufacturer installation requirements "
                "against approved plans."
            )
        }

    def floor_system_assembly(
            self,
            length_feet,
            width_feet,
            joist_spec,
            rim_spec,
            include_blocking=False,
            blocking_rows=1,
            joist_span_direction="length",
            waste_percent=None
    ):
        """Create a measured floor system from plan-specified members."""
        if not joist_spec or not rim_spec:
            raise ValueError(
                "Floor joist and rim specifications from the plan are required."
            )

        if joist_span_direction not in ["length", "width"]:
            raise ValueError(
                "Joist span direction must be either length or width."
            )

        joist_count_length = length_feet
        joist_count_width = width_feet
        blocking_run_length = width_feet

        if joist_span_direction == "width":
            # LumberEstimator counts joists across its width argument.
            # Swap the geometry so joists spanning the building width are
            # correctly counted across the building length.
            joist_count_length = width_feet
            joist_count_width = length_feet
            blocking_run_length = length_feet

        joists = self.lumber.floor_joists(
            joist_count_length,
            joist_count_width,
            joist_spec=joist_spec,
            waste_percent=waste_percent
        )
        rim_joists = self.lumber.rim_joists(
            length_feet,
            width_feet,
            rim_spec=rim_spec,
            waste_percent=joists["waste_percent"]
        )
        subfloor = self.lumber.subfloor_sheathing(
            length_feet,
            width_feet,
            waste_percent=joists["waste_percent"]
        )
        components = {
            "Floor joists": joists,
            "Rim joists": rim_joists,
            "Subfloor sheathing": subfloor
        }

        if include_blocking:
            components["Joist blocking"] = self.lumber.blocking(
                blocking_run_length,
                stud_spacing_inches=joist_spec["spacing_inches"],
                rows=blocking_rows,
                waste_percent=joists["waste_percent"],
                material_size=joist_spec["size"]
            )

        return {
            "type": "Residential Floor System Assembly",
            "dimensions": {
                "length": length_feet,
                "width": width_feet
            },
            "floor_area_sqft": round(length_feet * width_feet, 2),
            "joist_spec": joist_spec,
            "rim_spec": rim_spec,
            "joist_span_direction": joist_span_direction,
            "include_blocking": include_blocking,
            "blocking_rows": blocking_rows if include_blocking else 0,
            "waste_percent": joists["waste_percent"],
            "component_estimates": components,
            "material_takeoff": self._combine_material_takeoffs(
                *[
                    component["material_takeoff"]
                    for component in components.values()
                ]
            ),
            "assumptions": [
                "Joist size, member length, and spacing come from the approved framing plan.",
                "Rim material and stock length come from the approved framing plan.",
                "Subfloor uses 4x8 3/4 in T&G OSB coverage with the selected waste allowance."
            ],
            "exclusions": [
                "Beams, girders, posts, hangers, straps, adhesives, fasteners, and bridging unless separately estimated",
                "Bearing verification, point loads, openings, stair framing, and structural design",
                "Labor, permits, inspections, and local code review"
            ],
            "scope_note": (
                "Do not use this assembly to select structural members. "
                "Joist layout, rim detail, blocking, beams, connections, "
                "and openings must match approved framing plans."
            )
        }

    def interior_finish_assembly(
            self,
            net_wall_area_sqft,
            ceiling_area_sqft,
            include_insulation=False,
            insulation_r_value="R-13",
            include_drywall=True,
            include_primer_and_paint=True,
            flooring_area_sqft=0,
            flooring_type="Flooring",
            flooring_carton_coverage_sqft=20,
            baseboard_linear_feet=0,
            interior_door_quantity=0,
            interior_door_spec="Interior Door Unit"
    ):
        """Create a measured interior-finish assembly from plan takeoff areas."""
        if net_wall_area_sqft < 0 or ceiling_area_sqft < 0:
            raise ValueError("Wall and ceiling areas cannot be negative.")

        components = {}
        drywall_finish_area = net_wall_area_sqft + ceiling_area_sqft

        if include_insulation and net_wall_area_sqft > 0:
            components["Wall insulation"] = self.insulation.batt_insulation_area(
                net_wall_area_sqft,
                r_value=insulation_r_value
            )

        if include_drywall:
            if net_wall_area_sqft > 0:
                components["Wall drywall"] = self.drywall.wall_drywall_area(
                    net_wall_area_sqft
                )
            if ceiling_area_sqft > 0:
                components["Ceiling drywall"] = self.drywall.ceiling_drywall_area(
                    ceiling_area_sqft
                )
            if drywall_finish_area > 0:
                components.update(
                    {
                        "Joint compound": self.drywall_finish.joint_compound(
                            drywall_finish_area
                        ),
                        "Drywall tape": self.drywall_finish.drywall_tape(
                            drywall_finish_area
                        ),
                        "Drywall screws": self.drywall_finish.drywall_screws(
                            drywall_finish_area
                        ),
                        "Drywall sanding": self.drywall_finish.drywall_sanding(
                            drywall_finish_area
                        )
                    }
                )

        if include_primer_and_paint and drywall_finish_area > 0:
            components["Drywall primer"] = self.drywall_finish.primer(
                drywall_finish_area
            )

            if net_wall_area_sqft > 0:
                components["Interior wall paint"] = (
                    self.drywall_finish.interior_paint(
                        net_wall_area_sqft
                    )
                )

            if ceiling_area_sqft > 0:
                components["Ceiling paint"] = (
                    self.drywall_finish.ceiling_paint(
                        ceiling_area_sqft
                    )
                )

        if flooring_area_sqft > 0:
            components["Flooring"] = self.flooring(
                flooring_area_sqft,
                flooring_type=flooring_type,
                carton_coverage_sqft=flooring_carton_coverage_sqft
            )

        if baseboard_linear_feet > 0:
            components["Baseboard"] = self.baseboard(baseboard_linear_feet)

        if interior_door_quantity > 0:
            components["Interior doors"] = self.interior_doors(
                interior_door_quantity,
                door_spec=interior_door_spec
            )

        if not components:
            raise ValueError("Choose at least one interior finish component.")

        return {
            "type": "Interior Finish Assembly",
            "net_wall_area_sqft": round(net_wall_area_sqft, 2),
            "ceiling_area_sqft": round(ceiling_area_sqft, 2),
            "drywall_finish_area_sqft": round(drywall_finish_area, 2),
            "include_insulation": include_insulation,
            "insulation_r_value": insulation_r_value if include_insulation else None,
            "include_drywall": include_drywall,
            "include_primer_and_paint": include_primer_and_paint,
            "flooring_area_sqft": flooring_area_sqft,
            "flooring_type": flooring_type if flooring_area_sqft > 0 else None,
            "baseboard_linear_feet": baseboard_linear_feet,
            "interior_door_quantity": interior_door_quantity,
            "component_estimates": components,
            "material_takeoff": self._combine_material_takeoffs(
                *[
                    component["material_takeoff"]
                    for component in components.values()
                ]
            ),
            "assumptions": [
                "Wall and ceiling areas are net measured coverage areas from plans.",
                "Drywall finish and primer use combined measured wall and ceiling area; wall and ceiling paint are calculated separately.",
                "Flooring carton coverage and door specifications must match the selected products."
            ],
            "exclusions": [
                "Drywall texture, corner bead, trim profiles, hardware, transitions, and underlayment unless separately estimated",
                "Cabinets, countertops, tile, showers, appliances, labor, and permits",
                "Moisture conditions, substrate repairs, and manufacturer installation requirements"
            ],
            "scope_note": (
                "Verify room-by-room areas, ceiling heights, wet-area "
                "materials, door schedule, finish selections, and product "
                "coverage before ordering."
            )
        }

    #########################
    #### SPECIALTY WORK ####
    #########################

    def siding(self, wall_area_sqft, siding_type="Siding", waste_percent=None):
        return self.specialty.siding(
            wall_area_sqft,
            siding_type=siding_type,
            waste_percent=waste_percent
        )

    def housewrap(self, wall_area_sqft, roll_coverage_sqft=900, waste_percent=None):
        return self.specialty.housewrap(
            wall_area_sqft,
            roll_coverage_sqft=roll_coverage_sqft,
            waste_percent=waste_percent
        )

    def exterior_trim(self, linear_feet, trim_spec="1x4 Exterior Trim", board_length_feet=16, waste_percent=None):
        return self.specialty.exterior_trim(
            linear_feet,
            trim_spec=trim_spec,
            board_length_feet=board_length_feet,
            waste_percent=waste_percent
        )

    def windows(self, quantity, window_spec="Window Unit"):
        return self.specialty.windows(quantity, window_spec=window_spec)

    def exterior_doors(self, quantity, door_spec="Exterior Door Unit"):
        return self.specialty.exterior_doors(quantity, door_spec=door_spec)

    def decking(self, length, width, board_width_inches=5.5, board_length_feet=12, gap_inches=0.125, waste_percent=None):
        return self.specialty.decking(
            length,
            width,
            board_width_inches=board_width_inches,
            board_length_feet=board_length_feet,
            gap_inches=gap_inches,
            waste_percent=waste_percent
        )

    def fence(self, length, height, panel_width_feet=8, post_spacing_feet=8, waste_percent=None):
        return self.specialty.fence(
            length,
            height,
            panel_width_feet=panel_width_feet,
            post_spacing_feet=post_spacing_feet,
            waste_percent=waste_percent
        )

    def flooring(self, area_sqft, flooring_type="Flooring", carton_coverage_sqft=20, waste_percent=None):
        return self.specialty.flooring(
            area_sqft,
            flooring_type=flooring_type,
            carton_coverage_sqft=carton_coverage_sqft,
            waste_percent=waste_percent
        )

    def baseboard(self, linear_feet, board_length_feet=16, baseboard_spec="Baseboard Trim", waste_percent=None):
        return self.specialty.baseboard(
            linear_feet,
            board_length_feet=board_length_feet,
            baseboard_spec=baseboard_spec,
            waste_percent=waste_percent
        )

    def interior_doors(self, quantity, door_spec="Interior Door Unit"):
        return self.specialty.interior_doors(quantity, door_spec=door_spec)
