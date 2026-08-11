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
