""" 
Output_Calculation Class

"""

import glob
import logging
import pandas as pd
import geopandas as gpd
import fsspec
import boto3
import geopandas as gpd
import datetime as dt

from pyproj import CRS
from owslib.ogcapi.features import Features
from datetime import datetime, timedelta
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, EndpointConnectionError

# class imports
from Input_Reference import InputReference
from Input_VEDA import InputVEDA

class OutputCalculation():
    
    """ OutputCalculation
        Class representing output calculation of veda_input vs ref_input
    """
    
    # implemented output formats
    OUTPUT_FORMATS = ["txt", "json"]
    
    def __init__(self, 
                 veda_input: InputVEDA, 
                 ref_input: InputReference, 
                 output_format: str, 
                 output_maap_url: str,
                 print_on: bool,
                 plot_on: bool):

        # USER INPUT / FILTERS
        self._veda_input = veda_input
        self._ref_input = ref_input
        self._output_format = output_format
        self._output_maap_url = output_maap_url
        self._print_on = print_on
        self._plot_on = plot_on
        
        # PROGRAM SET
        self._polygons = None
        self._dump = None # content to dump into file
        
        # SINGLE SETUP
        self.__set_up_master()
        
    @property
    def veda_input(self):
        return self._veda_input
    
    @property
    def ref_input(self):
        return self._ref_input
    
    @property
    def polygons(self):
        return self._polygons
    
    # MASTER SET UP FUNCTION
    def __set_up_master(self):
        """ set up outputcalc instance with checks and generations; run main calculations"""
        
        assert self._output_format in OUTPUT_FORMATS, f"Provided output format {self._output_format} is NOT VALID, select only from implemented formats: {OUTPUT_FORMATS}"
        assert self.__set_up_valid_maap_url, f"Invalid URL: see assertions and/or possibly missing s3://maap-ops-workspace/shared/ in url. Provided url: {self._output_maap_url}"
        
        # generate file type based on format
        
        # veda and ref matching 
        
        # run calculations
        
        # write to outputs and call plots
        
        return self
    
    def __set_up_valid_maap_url(self):
        """ given a maap-ops-workspace url, check if valid with naming + s3 access"""
        
        maap_ops_contained ="s3://maap-ops-workspace/shared/" in self._output_maap_url
        
        try:
            # fetch s3 bucket and check if exists (not concerned w key since we will be making item)
            s3_url_parts = s3_url.split('/')
            if len(s3_url_parts) < 4 or s3_url_parts[0] != 's3:' or s3_url_parts[1] != '' or s3_url_parts[2] != '':
                return False

            bucket_name = s3_url_parts[3]
            s3 = boto3.client('s3')
            s3.head_bucket(Bucket=bucket_name)
            # s3.head_object(Bucket=bucket_name, Key=key)

            return True and maap_ops_contained
        
        except NoCredentialsError:
            print("AWS credentials not found. Please configure your AWS credentials.")
        except PartialCredentialsError:
            print("Incomplete AWS credentials found.")
        except EndpointConnectionError:
            print("Could not connect to the AWS endpoint. Please check your AWS configuration.")
        except Exception as e:
            print(f"Error: {str(e)}")

        return False
    
    
    def format_for_file(self):
        # TODO
        return 0
    
    def write_to_output_file(self):
        # TODO
        with fsspec.open(self._output_maap_url) as f:
            f.write(self._dump)

    
    #### WARNING: EXPERIMENTAL METHODS BELOW, NOT CONFORMING TO OOP DESIGN ###   
    
    # EXPERIMENTAL MATCHING
    def check_crs_match(self) -> bool:
        """ check both crs' are matching"""
        # TODO
        return True
    
    def find_closest_time_pairs(self):
        # nifc-perim pairs as tuples
        # i.e. (perimeter FEDS instance, NIFC match)
        comparison_pairs = []

        # per FEDS output perim -> get best NIFC match(es) by date
        print('Per FEDS output, identify best NIFC match...')
        for instance in tqdm(range(finalized_williams.shape[0])):

            # collection of indices relative to year_perims
            insc_indices = []
            # master matches with intersections/timestemp filtering
            intersd = []

            # iterate on all year_perims and inersect
            for insc in range(year_perims.shape[0]):
                # fetch nifc instance
                curr_nifc = year_perims.iloc[[insc]]
                intersect = gpd.overlay(curr_nifc,finalized_williams.iloc[[instance]], how='intersection')
                # cont if empty
                if not intersect.empty:
                    insc_indices.append(insc)
                # else: continue

            if len(insc_indices) == 0:
                print('WARNING: insc_indices was none -> skipping step')
                continue

            # all current indices present get_nearest check opportunities
            timestamp = finalized_williams.iloc[[instance]].t
            # apply insc_indices to pick out intersect matches
            reduced = year_perims.take(insc_indices)
            # match run with get nearest
            # although its really picky -> try for now

            # print(f'VERBOSE: reduced: {reduced}, timestamp: {timestamp}')
            try:
                matches = PerimFuncs.get_nearest(reduced, timestamp, PerimConsts.curr_dayrange)
            except:
                # print('WARNING get_nearest failed: continue in instance comparison')
                # indicates no match in given range -> append to failure list 
                print(f'WARNING: Perim master row ID: {finalized_williams.iloc[[instance]].index} at index {instance} as NO INTERSECTIONS at closest date. Storing and will report 0 accuracy.')
                comparison_pairs.append((finalized_williams.iloc[[instance]], None))
                continue

            # all matches should act as intersd -> extract from DF
            if matches is None:
                # @TODO: improve handling -> likely just continue and report failed benching
                raise Exception('FAILED: No matching dates found even with 7 day window, critical benchmarking failure.')

            intersd = [matches.iloc[[ing]] for ing in range(matches.shape[0])]

            if matches is None:
                # @TODO: improve handling -> likely just continue and report failed benching
                raise Exception('FAILED: No matching dates found even with 7 day window, critical benchmarking failure.')

            if len(intersd) == 0:
                # print(f'WARNING: Perim master row ID: {finalized_williams.iloc[[instance]].index} at index {instance} as NO INTERSECTIONS at closest date. Storing and will report 0 accuracy.')
                # comparison_pairs.append((finalized_williams.iloc[[instance]], None))
                assert 1==0, "case shouldn't exist, throw exception"

            elif len(intersd) > 1:
                # if multiple have overlay -> store them with a warning 
                print(f'NOTICE: More thane 1, in total: {len(matches)} NIFC date matches, intersect with perimeter master row ID: {finalized_williams.iloc[[instance]].index} with index in finalized_willaims: {instance}, storing all as pairs')

                # iterate and generate tuple pairs; append to list
                [comparison_pairs.append((finalized_williams.iloc[[instance]], to_ap)) for to_ap in intersd]

            else:
                # single match -> append (perim instance, NIFC single match)
                comparison_pairs.append((finalized_williams.iloc[[instance]], intersd[0]))
        
    
    # EXPERIMENTAL CALCULATION METHODS
    def simplify_geometry(shape, tolerance):
        """ shape: to simplify
            tolerance: passed to shapely tol
            return: simplified shape
        """
        # keep preserve_topology as default (true)
        assert isinstance(shape, gpd.GeoDataFrame)
        return shape.geometry.simplify(tolerance)

    # @TODO: finish implementing recursive function on simplification calc
    def best_simplification (feds, nifc, 
                             top_performance, 
                             top_tolerance, 
                             base_tolerance, 
                             calc_method, 
                             lowerPref):
        """ feds: feds source
            nifc: external source to compare to
            top_performance: best numeric value (default is worst value aka > 100 % error)
            top_tolerance: corresponding simplification with best performance
            base_tolerance: counter for tracking progress from limit -> 0
            calc_method
            lowerPref: true if a "better" score is considered a lower value

            return: top_tolerance (best tolerance value from recursion)

        """
        if base_tolerance == 0:
            return top_tolerance

        # simplify + calculate performance
        simplified_feds = simplify_geometry(feds, base_tolerance)
        curr_performance = calc_method(simplified_feds, nifc)

        # if performance "better" (depends on passed bool / method) -> persist
        if curr_performance < top_performance and lowerPref:
            top_performance = curr_performance
            top_tolerance = base_tolerance
        elif curr_performance > top_performance and not lowerPref:
            top_performance = curr_performance
            top_tolerance = base_toleranc

        # reduce and keep recursing down
        base_tolerance -= 1

        return best_simplification(feds, nifc, top_performance, top_tolerance, base_tolerance, calc_method, lowerPref)


    def areaCalculation(geom_instance):
        """ Calculate area of the object, including
            mult-row instances via loop
            Input: geom data frame instance
            Output: numeric area calculation (units defined in const)
            
            # terms:
            # FEDS data are considered as the predicted class. 
            # TN: True Negative; FN: False Negative; FP: False Positive; 
            # TP: True Positive; FEDS_UB: Unburned area from FEDS; 
            # FEDS_B: Area burned from FEDS; FRAP_UB: Unburned area from FRAP; 
            # FRAP_B: Burned area from FRAP; AREA_TOTAL: Total land area in CA
        """
        try:
            area = 0
            for i in range(geom_instance.geometry.area.shape[0]):
                area += geom_instance.geometry.area[i]
        except KeyError:
            # print('Identified key error in areaCalculation(): returning item() based area calc', end='\r')
            area = geom_instance.geometry.area.item()

        return area

    def truePos(feds_inst, nifc_inst):
        """ Calculate true pos area:
            where both NIFC and FEDS burned
            return basic intersection
        """
        overlay = gpd.overlay(feds_inst, nifc_inst, how='intersection')
        result = areaCalculation(overlay) # overlay.geometry.area.item()
        return result

    def falseNeg(feds_inst, nifc_inst):
        """ Calculate false negative area:
            NIFC burned but FEDS DID NOT burn (unburned needs envelope)
            make bounding -> get negative of Feds -> intersect with nifc (burning)
        """
        # union to envelope 
        unionr = gpd.overlay(feds_inst, nifc_inst, how='union')

        # generate bounding box fitting both instances (even if multi-poly)
        net_bounding = unionr.geometry.envelope
        # net_barea = areaCalculation(net_bounding)
        # convert to data frame
        net_bounding = net_bounding.to_frame()

        feds_neg = gpd.overlay(net_bounding, feds_inst, how='difference')
        result = gpd.overlay(feds_neg, nifc_inst, keep_geom_type=False, how='intersection')
        result = areaCalculation(result)

        return result

    def falsePos(feds_inst, nifc_inst):
        """ Calculate false negative area:
            NIFC DID NOT burn (unburned needs envelope) but FEDS burned 
            bounding -> get negative of nifc -> intersect with feds (burning)
        """
        # union to envelope 
        unionr = gpd.overlay(feds_inst, nifc_inst, how='union')

        # generate bounding box fitting both instances (even if multi-poly)
        net_bounding = unionr.geometry.envelope
        # net_barea = areaCalculation(net_bounding)
        # convert to data frame
        net_bounding = net_bounding.to_frame()

        nifc_neg = gpd.overlay(net_bounding, nifc_inst, how='difference')

        result = gpd.overlay(nifc_neg, feds_inst, keep_geom_type=False, how='intersection')
        result = areaCalculation(result)

        return result

    def trueNeg(feds_inst, nifc_inst):
        """ Calculate true negative area (agreeing on none geom)
            input: two geo dataframes
            output: area where both agree of no geom
        """

        # union to envelope 
        unionr = gpd.overlay(feds_inst, nifc_inst, how='union')

        # generate bounding box fitting both instances (even if multi-poly)
        net_bounding = unionr.geometry.envelope
        net_barea = areaCalculation(net_bounding)
        # convert to data frame
        net_bounding = net_bounding.to_frame()

        # subtract feds_inst and nifc_inst from bounding area
        feds_neg = gpd.overlay(net_bounding, feds_inst, how='difference')
        nifc_neg = gpd.overlay(net_bounding, nifc_inst, how='difference')

        # TN = calculate intersection of both "negatives"
        inter_neg = gpd.overlay(feds_neg, nifc_neg, keep_geom_type=False, how='intersection')
        result = areaCalculation(inter_neg)

        return result

    def areaTotal(feds_inst, nifc_inst):
        """ Calculate total Area defined in table 6:	
            FEDS_B/REF_B(burned area)
        """
        # union to envelope 
        unionr = gpd.overlay(feds_inst, nifc_inst, how='union')
        # generate bounding box fitting both instances (even if multi-poly)
        net_bounding = unionr.geometry.envelope
        net_barea = areaCalculation(net_bounding)
        # convert to data frame
        # net_bounding = net_bounding.to_frame()

        return net_barea

    def ratioCalculation(feds_inst, nifc_inst):
        """ Calculate ratio defined in table 6:	
            FEDS_B/REF_B(burned area)
        """
        # sum area (since mul entries may exist) up by calc
        feds_area = areaCalculation(feds_inst)
        nifc_area = areaCalculation(nifc_inst)

        assert feds_area is not None, "None type detected for area; something went wrong"
        assert nifc_area is not None, "None type detected for area; something went wrong"

        return feds_area / nifc_area

    def accuracyCalculation(feds_inst, nifc_inst):
        """ Calculate accuracy defined in table 6:
            (TP+TN)/AREA_TOTAL

            TN == agreed inverse by bounding box
            TP == FRAP + FEDS agree on burned (intersect)
        """
        TN = trueNeg(feds_inst, nifc_inst)
        TP = truePos(feds_inst, nifc_inst)
        AREA_TOTAL = areaTotal(feds_inst, nifc_inst)

        return (TN + TP) / AREA_TOTAL

    # @TODO: call percision calculation func
    def precisionCalculation(feds_inst, nifc_inst):
        """ TP/FEDS_B
            TP == FRAP + FEDS agree on burned (intersect)
            FEDS_B == all burned of feds 
        """
        assert isinstance(feds_inst, pd.DataFrame) and isinstance(nifc_inst, pd.DataFrame), "Object types will fail intersection calculation; check inputs"
        # calculate intersect (agreement) -> divide
        # overlay = gpd.overlay(feds_inst, nifc_inst, how='intersection')
        TP = truePos(feds_inst, nifc_inst)
        feds_area = areaCalculation(feds_inst)

        return TP / feds_area

    def recallCalculation(feds_inst, nifc_inst):
        """ TP/REF_B (nifc)
            TP == FRAP + FEDS agree on burned (intersect)
            REF_B == all burned of nifc/source
        """
        # overlay = gpd.overlay(feds_inst, nifc_inst, how='intersection')
        TP = truePos(feds_inst, nifc_inst)
        nifc_area = areaCalculation(nifc_inst)

        return TP / nifc_area

    def IOUCalculation(feds_inst, nifc_inst):
        """ IOU (inter over union)
            TP/(TP + FP + FN)
        """

        # overlay = gpd.overlay(feds_inst, nifc_inst, how='intersection')
        TP = truePos(feds_inst, nifc_inst)
        FP = falsePos(feds_inst, nifc_inst) # feds + nifc agree on no burning
        FN = falseNeg(feds_inst, nifc_inst) # feds thinks unburned when nifc burned

        return 0

    def f1ScoreCalculation(feds_inst, nifc_inst):
        """ 2 * (Precision * Recall)/(Precision + Recall)
        """
        precision = precisionCalculation(feds_inst, nifc_inst)
        recall = recallCalculation(feds_inst, nifc_inst)
        calc = 2 * (precision*recall)/(precision+recall)

        return calc

    # @TODO: custom calc functions
    def symmDiffRatioCalculation(feds_inst, nifc_inst):
        """ symmetric difference calc, ratio 
            NOTE: error relative to NIFC/external soure
        """
        sym_diff = feds_inst.symmetric_difference(nifc_inst, align=False)
        # use item() to fetch int out of values
        assert sym_diff.shape[0] == 1, "Multiple sym_diff entries identified; pair accuracy evaluation will fail."
        # calculate error percent: (difference / "correct" shape aka nifc)
        symm_area = areaCalculation(sym_diff)
        nifc_area = areaCalculation(nifc_inst)
        # symmDiff_ratio = sym_diff.geometry.area.item() / nifc_inst.geometry.area.item()
        symmDiff_ratio = symm_area / nifc_area

        return symmDiff_ratio