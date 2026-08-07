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
            waste_percent=10
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
            waste_percent=10,
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
            waste_percent=10
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
            waste_percent=10
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
            waste_percent=10
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
            waste_percent=10
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
            waste_percent=10
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
            waste_percent=10
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
            waste_percent=10
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
            waste_percent=10
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
            waste_percent=10
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
            waste_percent=10
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
            waste_percent=10
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

    def concrete_trench(self, length, width_inches, depth_inches, waste_percent=10):
        return self.concrete.concrete_trench(
            length,
            width_inches,
            depth_inches,
            waste_percent
        )

    def concrete_retaining_wall(self, length, height, thickness_inches, waste_percent=10):
        return self.concrete.concrete_retaining_wall(
            length,
            height,
            thickness_inches,
            waste_percent
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
            waste_percent=10
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

    def concrete_spread_footing(self, length, width, depth_inches, waste_percent=10):
        return self.concrete.concrete_spread_footing(
            length,
            width,
            depth_inches,
            waste_percent
        )

    def concrete_round_footing(self, diameter_inches, depth, quantity=1, waste_percent=10):
        return self.concrete.concrete_round_footing(
            diameter_inches,
            depth,
            quantity,
            waste_percent
        )

    def concrete_pile_cap(self, length, width, depth_inches, waste_percent=10):
        return self.concrete.concrete_pile_cap(
            length,
            width,
            depth_inches,
            waste_percent
        )

    def concrete_lintel(self, length, width_inches, height_inches, waste_percent=10):
        return self.concrete.concrete_lintel(
            length,
            width_inches,
            height_inches,
            waste_percent
        )

    def concrete_slab_edge(
            self,
            length,
            width,
            edge_width_inches,
            edge_depth_inches
    ):
        return self.concrete.concrete_slab_edge(
            length,
            width,
            edge_width_inches,
            edge_depth_inches
        )


    ################
    #### LUMBER ####
    ################

    def frame_wall(
            self,
            length_feet,
            height_feet,
            stud_spacing_inches=16
    ):
        return self.lumber.frame_wall(
            length_feet,
            height_feet,
            stud_spacing_inches
        )

    def ceiling_joists(self, length, width, joist_spec=None):
        return self.lumber.ceiling_joists(
            length,
            width,
            joist_spec=joist_spec
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

    def ridge_board(self, length, ridge_spec=None):
        return self.lumber.ridge_board(
            length,
            ridge_spec=ridge_spec
        )

    def collar_ties(self, length, tie_spec=None):
        return self.lumber.collar_ties(
            length,
            tie_spec=tie_spec
        )

    def roof_sheathing(self, length, width):
        return self.lumber.roof_sheathing(
            length,
            width
        )

    def wall_sheathing(self, length, height):
        return self.lumber.wall_sheathing(
            length,
            height
        )

    def headers(self, opening_width, header_spec=None):
        return self.lumber.headers(
            opening_width,
            header_spec=header_spec
        )

    def blocking(self, length):
        return self.lumber.blocking(
            length
        )

    def subfloor_sheathing(self, length, width):
        return self.lumber.subfloor_sheathing(
            length,
            width
        )

    def rim_joists(self, length, width, rim_spec=None):
        return self.lumber.rim_joists(
            length,
            width,
            rim_spec=rim_spec
        )

    def shingles(self, length, width):
        return self.roofing.shingles(
            length,
            width
        )

    def underlayment(self, length_feet, width_feet):
        return self.roofing.underlayment(
            length_feet,
            width_feet
        )

    def drip_edge(self, required_length_feet):
        return self.roofing.drip_edge(
            required_length_feet
        )

    def ice_water_shield(self, required_coverage_sqft):
        return self.roofing.ice_water_shield(
            required_coverage_sqft
        )

    def ridge_vent(self, length_feet):
        return self.roofing.ridge_vent(
            length_feet
        )

    def flashing(self, quantity):
        return self.roofing.flashing(
            quantity
        )

    def studs(self,wall_length,wall_height,stud_spacing_inches=16):
        return self.lumber.studs(
            wall_length,
            wall_height,
            stud_spacing_inches)

    def king_studs(self,openings,wall_height):
        return self.lumber.king_studs(
            openings,
            wall_height
        )

    def jack_studs(self,openings,opening_height):
        return self.lumber.jack_studs(
            openings,
            opening_height
        )

    def cripple_studs(self,openings,opening_width,stud_spacing_inches=16):
        return self.lumber.cripple_studs(
            openings,
            opening_width,
            stud_spacing_inches
        )

    def corner_posts(self,corners,wall_height):
        return self.lumber.corner_posts(
            corners,
            wall_height
        )

    def plates(self,length,plate_type="double top"):
        return self.lumber.plates(
            length,
            plate_type
        )

    def sill_plate(self,length):
        return self.lumber.sill_plate(
            length
        )

    def posts(self, quantity, height, post_spec=None):
        return self.lumber.posts(
            quantity,
            height,
            post_spec=post_spec
        )

    def beams(self, length, beam_spec=None):
        return self.lumber.beams(
            length,
            beam_spec=beam_spec
        )


    #################
    #### DRYWALL ####
    #################

    def wall_drywall(
            self,
            length,
            height,
            quantity=1
    ):
        return self.drywall.wall_drywall(
            length,
            height,
            quantity=quantity
        )

    def ceiling_drywall(self, length, width):
        return self.drywall.ceiling_drywall(
            length,
            width
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
            quantity=1
    ):
        return self.insulation.batt_insulation(
            length,
            height,
            r_value=r_value,
            stud_spacing=stud_spacing,
            quantity=quantity
        )

    def blown_insulation(
            self,
            length,
            width,
            r_value="R-38"
    ):
        return self.insulation.blown_insulation(
            length,
            width,
            r_value=r_value
        )

    def spray_foam(
            self,
            length,
            height,
            thickness_inches,
            coverage_per_kit_sqft
    ):
        return self.insulation.spray_foam(
            length,
            height,
            thickness_inches=thickness_inches,
            coverage_per_kit_sqft=coverage_per_kit_sqft
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