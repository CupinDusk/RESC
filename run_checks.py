"""Recompute the old frozen choices and new conditional order audit."""
from pathlib import Path
import argparse,hashlib,json,math,os,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
def compare(a,b,path='root'):
    if type(b) is float:assert type(a) in [int,float] and math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-12),path
    elif isinstance(b,dict):
        assert isinstance(a,dict) and set(a)==set(b),path
        for k in b:compare(a[k],b[k],path+'.'+k)
    elif isinstance(b,list):
        assert isinstance(a,list) and len(a)==len(b),path
        for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+'['+str(i)+']')
    else:assert a==b,path
def main():
    p=argparse.ArgumentParser();p.add_argument('--scipy-path');p.add_argument('--fetch-ordersage',action='store_true');a=p.parse_args()
    m=json.loads((HERE/'MANIFEST.json').read_text(encoding='utf-8'))
    for n,h in m['files'].items():assert hashlib.sha256((HERE/n).read_bytes()).hexdigest()==h,n
    env=os.environ.copy()
    if a.scipy_path:env['PYTHONPATH']=a.scipy_path+os.pathsep+env.get('PYTHONPATH','')
    generated=HERE/'generated/reanalysis';assert not generated.exists(),'Use a fresh extraction';generated.mkdir(parents=True)
    old=HERE/'artifacts/hopper-retained-v1'
    for f in old.iterdir():
        if f.is_file():shutil.copyfile(f,generated/f.name)
    run=subprocess.run([sys.executable,'-B','-X','utf8',str(generated/'reanalyze.py')],env=env,capture_output=True,text=True,timeout=120)
    (HERE/'generated/reanalysis.log').write_text(run.stdout+'\n'+run.stderr,encoding='utf-8');assert run.returncode==0,run.stderr
    compare(json.loads((generated/'recomputed-results.json').read_text(encoding='utf-8')),json.loads((old/'recomputed-results.json').read_text(encoding='utf-8')))
    run=subprocess.run([sys.executable,'-B','-X','utf8',str(HERE/'analysis/hopper_order_sensitivity.py')],env=env,capture_output=True,text=True,timeout=240)
    (HERE/'generated/order-audit.log').write_text(run.stdout+'\n'+run.stderr,encoding='utf-8');assert run.returncode==0,run.stderr
    actual=json.loads((HERE/'analysis/HOPPER_ORDER_SENSITIVITY_RESULTS.json').read_text(encoding='utf-8'))
    expected=json.loads((HERE/'expected/HOPPER_ORDER_SENSITIVITY_RESULTS.json').read_text(encoding='utf-8'));compare(actual,expected)
    run=subprocess.run([sys.executable,'-B','-X','utf8',str(HERE/'analysis/hopper_model_comparison.py')],env=env,capture_output=True,text=True,timeout=240)
    (HERE/'generated/model-comparison.log').write_text(run.stdout+'\n'+run.stderr,encoding='utf-8');assert run.returncode==0,run.stderr
    model_actual=json.loads((HERE/'analysis/HOPPER_R5_MODEL_RESULTS.json').read_text(encoding='utf-8'))
    model_expected=json.loads((HERE/'expected/HOPPER_R5_MODEL_RESULTS.json').read_text(encoding='utf-8'));compare(model_actual,model_expected)
    run=subprocess.run([sys.executable,'-B','-X','utf8',str(HERE/'analysis/hopper_anchor_audit.py')],env=env,capture_output=True,text=True,timeout=240)
    (HERE/'generated/anchor-audit.log').write_text(run.stdout+'\n'+run.stderr,encoding='utf-8');assert run.returncode==0,run.stderr
    anchor_actual=json.loads((HERE/'analysis/HOPPER_R6_ANCHOR_RESULTS.json').read_text(encoding='utf-8'))
    compare(anchor_actual,json.loads((HERE/'expected/HOPPER_R6_ANCHOR_RESULTS.json').read_text(encoding='utf-8')))
    external='NOT_RUN_REQUIRES_EXPLICIT_FETCH_FLAG'
    if a.fetch_ordersage:
        run=subprocess.run([sys.executable,'-B','-X','utf8',str(HERE/'analysis/fetch_ordersage_schemas.py')],env=env,capture_output=True,text=True,timeout=300)
        (HERE/'generated/external-fetch.log').write_text(run.stdout+'\n'+run.stderr,encoding='utf-8');assert run.returncode==0,run.stderr
        compare(json.loads((HERE/'analysis/external-ordersage-inputs/MANIFEST.json').read_text(encoding='utf-8')),json.loads((HERE/'expected/ORDERSAGE_INPUT_MANIFEST.json').read_text(encoding='utf-8')))
        run=subprocess.run([sys.executable,'-B','-X','utf8',str(HERE/'analysis/ordersage_secondary.py')],env=env,capture_output=True,text=True,timeout=120)
        (HERE/'generated/external-assessment.log').write_text(run.stdout+'\n'+run.stderr,encoding='utf-8');assert run.returncode==0,run.stderr
        compare(json.loads((HERE/'analysis/ORDERSAGE_SECONDARY_RESULTS.json').read_text(encoding='utf-8')),json.loads((HERE/'expected/ORDERSAGE_SECONDARY_RESULTS.json').read_text(encoding='utf-8')))
        external='PASS_PUBLISHED_INPUTS_AND_ALL_FROZEN_ASSESSMENT_RESULTS'
    run=subprocess.run([sys.executable,'-B','-X','utf8',str(HERE/'analysis/hopper_joint_queries.py')],env=env,capture_output=True,text=True,timeout=300)
    (HERE/'generated/joint-query-audit.log').write_text(run.stdout+'\n'+run.stderr,encoding='utf-8');assert run.returncode==0,run.stderr
    joint_actual=json.loads((HERE/'analysis/HOPPER_R7_JOINT_RESULTS.json').read_text(encoding='utf-8'))
    compare(joint_actual,json.loads((HERE/'expected/HOPPER_R7_JOINT_RESULTS.json').read_text(encoding='utf-8')))
    calibration_reference='NOT_RUN_REQUIRES_EXPLICIT_FETCH_FLAG'
    if a.fetch_ordersage:
        run=subprocess.run([sys.executable,'-B','-X','utf8',str(HERE/'analysis/hopper_calibration_reference.py')],env=env,capture_output=True,text=True,timeout=120)
        (HERE/'generated/calibration-reference.log').write_text(run.stdout+'\n'+run.stderr,encoding='utf-8');assert run.returncode==0,run.stderr
        ref_actual=json.loads((HERE/'analysis/HOPPER_R7_CALIBRATION_REFERENCE_RESULTS.json').read_text(encoding='utf-8'))
        assert len(ref_actual['ufs_point_queries'].pop('queries'))==50
        compare(ref_actual,json.loads((HERE/'expected/HOPPER_R7_CALIBRATION_REFERENCE_RESULTS.json').read_text(encoding='utf-8')))
        calibration_reference='PASS_ALL_STATIONARY_SCENARIOS_AND_FIVE_DEPENDENT_SPLITS'
    run=subprocess.run([sys.executable,'-B','-X','utf8',str(HERE/'analysis/hopper_explanation_radius.py')],env=env,capture_output=True,text=True,timeout=300)
    (HERE/'generated/explanation-radius.log').write_text(run.stdout+'\n'+run.stderr,encoding='utf-8');assert run.returncode==0,run.stderr
    radius_actual=json.loads((HERE/'analysis/HOPPER_R8_RADIUS_RESULTS.json').read_text(encoding='utf-8'))
    radius_expected=json.loads((HERE/'expected/HOPPER_R8_RADIUS_RESULTS.json').read_text(encoding='utf-8'))
    # Optimum witnesses need not be unique. The script validates feasibility;
    # compare all deterministic classifications/values, not the chosen vertex.
    def remove_vertices(v):
        if isinstance(v,dict):return {k:remove_vertices(x) for k,x in v.items() if k not in ['witness','attaining_witness']}
        if isinstance(v,list):return [remove_vertices(x) for x in v]
        return v
    compare(remove_vertices(radius_actual),remove_vertices(radius_expected))
    run=subprocess.run([sys.executable,'-B','-X','utf8',str(HERE/'analysis/hopper_partial_orders.py')],env=env,capture_output=True,text=True,timeout=600)
    (HERE/'generated/partial-orders.log').write_text(run.stdout+'\n'+run.stderr,encoding='utf-8');assert run.returncode==0,run.stderr
    order_actual=json.loads((HERE/'analysis/HOPPER_R9_ORDER_RESULTS.json').read_text(encoding='utf-8'))
    order_expected=json.loads((HERE/'expected/HOPPER_R9_ORDER_RESULTS.json').read_text(encoding='utf-8'))
    # LP optimum vertices and sub-tolerance roundoff signs need not be unique.
    # Compare every nondegenerate count/value and ALL64080 CSV optima numerically.
    def order_stable(v):
        skip=['witness','attaining_witness','attaining_original_LP_witness','complete_csv_sha256','small_positive_differences_at_or_below_1e-10','positive_windows_at_or_below_1e-10']
        if isinstance(v,dict):return {k:order_stable(x) for k,x in v.items() if k not in skip}
        if isinstance(v,list):return [order_stable(x) for x in v]
        return v
    compare(order_stable(order_actual),order_stable(order_expected))
    import csv
    with (HERE/'analysis/HOPPER_R9_ALL_TOTAL_ORDERS.csv').open(encoding='utf-8',newline='') as f:got=list(csv.DictReader(f))
    with (HERE/'expected/HOPPER_R9_ALL_TOTAL_ORDERS.csv').open(encoding='utf-8',newline='') as f:want=list(csv.DictReader(f))
    assert len(got)==len(want)==64080
    numeric=['all_anchor_radius','shared_path_radius','window_width','ratio']
    for actual_row,expected_row in zip(got,want):
        assert set(actual_row)==set(expected_row)
        for key in actual_row:
            if key in numeric:
                if not expected_row[key]:assert not actual_row[key]
                else:compare(float(actual_row[key]),float(expected_row[key]),'all_order_csv.'+key)
            else:assert actual_row[key]==expected_row[key]
    run=subprocess.run([sys.executable,'-B','-X','utf8',str(HERE/'analysis/hopper_h20_certificate.py')],env=env,capture_output=True,text=True,timeout=30)
    (HERE/'generated/H20-certificate.log').write_text(run.stdout+'\n'+run.stderr,encoding='utf-8');assert run.returncode==0,run.stderr
    compare(json.loads((HERE/'analysis/HOPPER_R9_H20_CERTIFICATE.json').read_text(encoding='utf-8')),json.loads((HERE/'expected/HOPPER_R9_H20_CERTIFICATE.json').read_text(encoding='utf-8')))
    for script,logname in [('hopper_exact_certificates.py','exact-certificates'),('hopper_full_order_tightness.py','complete-order-sharpness')]:
        run=subprocess.run([sys.executable,'-B','-X','utf8',str(HERE/'analysis'/script)],env=env,capture_output=True,text=True,timeout=600)
        (HERE/('generated/'+logname+'.log')).write_text(run.stdout+'\n'+run.stderr,encoding='utf-8');assert run.returncode==0,run.stderr
    run=subprocess.run([sys.executable,'-B','-X','utf8',str(HERE/'analysis/hopper_exact_certificates.py'),'--verify-certificates'],env=env,capture_output=True,text=True,timeout=120)
    (HERE/'generated/exact-certificate-replay.log').write_text(run.stdout+'\n'+run.stderr,encoding='utf-8');assert run.returncode==0,run.stderr
    exact_actual=json.loads((HERE/'analysis/HOPPER_R10_EXACT_RESULTS.json').read_text(encoding='utf-8'))
    exact_expected=json.loads((HERE/'expected/HOPPER_R10_EXACT_RESULTS.json').read_text(encoding='utf-8'))
    # Historical LP float text/hash/minimum can vary by sub-tolerance bits;
    # exact generated cycle/potential certificates and their hash MUST match.
    def exact_stable(v):
        if isinstance(v,dict):return {k:exact_stable(x) for k,x in v.items() if k not in ['historical_numeric_csv_sha256','historical_minimum_width_above_1e-10']}
        if isinstance(v,list):return [exact_stable(x) for x in v]
        return v
    assert exact_stable(exact_actual)==exact_stable(exact_expected)
    assert exact_actual['certificate_sha256']==exact_expected['certificate_sha256']
    full_actual=json.loads((HERE/'analysis/HOPPER_R10_FULL_ORDER_RESULTS.json').read_text(encoding='utf-8'))
    full_expected=json.loads((HERE/'expected/HOPPER_R10_FULL_ORDER_RESULTS.json').read_text(encoding='utf-8'))
    compare(full_actual,full_expected)
    run=subprocess.run([sys.executable,'-B','-X','utf8',str(HERE/'analysis/hopper_scalar_archive.py')],env=env,capture_output=True,text=True,timeout=120)
    (HERE/'generated/scalar-archive.log').write_text(run.stdout+'\n'+run.stderr,encoding='utf-8');assert run.returncode==0,run.stderr
    archive_actual=json.loads((HERE/'analysis/HOPPER_R12_ARCHIVE_RESULTS.json').read_text(encoding='utf-8'))
    compare(archive_actual,json.loads((HERE/'expected/HOPPER_R12_ARCHIVE_RESULTS.json').read_text(encoding='utf-8')))
    matching_actual=None
    for script,result_name,timeout in [('hopper_ranking_factor.py','HOPPER_R13_MATCHING_RESULTS.json',600),('hopper_r13_worked_order.py','HOPPER_R13_WORKED_ORDER_RESULTS.json',120)]:
        run=subprocess.run([sys.executable,'-B','-X','utf8',str(HERE/'analysis'/script)],env=env,capture_output=True,text=True,timeout=timeout)
        (HERE/'generated'/(script+'.log')).write_text(run.stdout+'\n'+run.stderr,encoding='utf-8');assert run.returncode==0,run.stderr
        new_actual=json.loads((HERE/'analysis'/result_name).read_text(encoding='utf-8'))
        expected=json.loads((HERE/'expected'/result_name).read_text(encoding='utf-8'))
        # Historical LP CSV bits are not exact certificates. Compare their
        # numerical values through the existing tolerance, and exact witnesses
        # without converting rational strings to approximate numbers.
        for v in [new_actual,expected]:
            v.pop('retained_input_csv_sha256',None);v.pop('matching_results_sha256',None)
        compare(new_actual,expected)
        if script=='hopper_ranking_factor.py':matching_actual=new_actual
    run=subprocess.run([sys.executable,'-B','-X','utf8',str(HERE/'analysis/hopper_quartet_exactness.py')],env=env,capture_output=True,text=True,timeout=120)
    (HERE/'generated/quartet-exactness.log').write_text(run.stdout+'\n'+run.stderr,encoding='utf-8');assert run.returncode==0,run.stderr
    quartet_actual=json.loads((HERE/'analysis/HOPPER_R14_QUARTET_RESULTS.json').read_text(encoding='utf-8'))
    quartet_expected=json.loads((HERE/'expected/HOPPER_R14_QUARTET_RESULTS.json').read_text(encoding='utf-8'))
    for v in [quartet_actual,quartet_expected]:v.pop('matching_results_sha256',None)
    compare(quartet_actual,quartet_expected)
    run=subprocess.run([sys.executable,'-B','-X','utf8',str(HERE/'analysis/hopper_planned_auditor.py')],env=env,capture_output=True,text=True,timeout=300)
    (HERE/'generated/planned-auditor.log').write_text(run.stdout+'\n'+run.stderr,encoding='utf-8');assert run.returncode==0,run.stderr
    auditor_actual=json.loads((HERE/'analysis/HOPPER_R14_AUDITOR_RESULTS.json').read_text(encoding='utf-8'))
    auditor_expected=json.loads((HERE/'expected/HOPPER_R14_AUDITOR_RESULTS.json').read_text(encoding='utf-8'))
    for v in [auditor_actual,auditor_expected]:v.pop('matching_results_sha256',None)
    compare(auditor_actual,auditor_expected)
    for script,result_name in [('hopper_quartet_auditor.py','HOPPER_R16_QUARTET_AUDITOR_RESULTS.json'),('verify_r15_compact_witness.py','HOPPER_R15_COMPACT_WITNESS_CHECK.json')]:
        run=subprocess.run([sys.executable,'-B','-X','utf8',str(HERE/'analysis'/script)],env=env,capture_output=True,text=True,timeout=120)
        (HERE/'generated'/(script+'.log')).write_text(run.stdout+'\n'+run.stderr,encoding='utf-8');assert run.returncode==0,run.stderr
        got=json.loads((HERE/'analysis'/result_name).read_text(encoding='utf-8'))
        want=json.loads((HERE/'expected'/result_name).read_text(encoding='utf-8'))
        # These two provenance hashes include historical LP text bits. The
        # old stage compares their science numerically, with exact certificates.
        # New route CSV hash and all rational witness coordinates MUST match.
        for value in [got,want]:
            value.pop('previous_auditor_result_sha256',None);value.pop('input_r13_result_sha256',None)
        compare(got,want)
        if script=='hopper_quartet_auditor.py':quartet_only_actual=got
    run=subprocess.run([sys.executable,'-B','-X','utf8',str(HERE/'analysis/hopper_r18_exposition.py')],env=env,capture_output=True,text=True,timeout=120)
    (HERE/'generated/two-clause-gap-exposition.log').write_text(run.stdout+'\n'+run.stderr,encoding='utf-8');assert run.returncode==0,run.stderr
    exposition=json.loads((HERE/'analysis/HOPPER_R18_EXPOSITION_RESULTS.json').read_text(encoding='utf-8'))
    assert exposition==json.loads((HERE/'expected/HOPPER_R18_EXPOSITION_RESULTS.json').read_text(encoding='utf-8'))
    for script,result_name in [('route_ablation.py','ROUTE_ABLATION_RESULTS.json'),('make_separate_witnesses.py','SEPARATE_PATH_WITNESSES.json')]:
        run=subprocess.run([sys.executable,'-B','-X','utf8',str(HERE/'analysis'/script)],env=env,capture_output=True,text=True,timeout=120)
        (HERE/'generated'/(script+'.log')).write_text(run.stdout+'\n'+run.stderr,encoding='utf-8');assert run.returncode==0,run.stderr
        got=json.loads((HERE/'analysis'/result_name).read_text(encoding='utf-8'))
        want=json.loads((HERE/'expected'/result_name).read_text(encoding='utf-8'))
        assert got==want,result_name
    result={'result':'PASS_TWO_CLAUSE_GAP_EXPOSITION_AND_ALL_PRIOR_CHECKS','input_files_verified':len(m['files']),
        'old_numeric_reanalysis':'PASS','new_conditional_audit':'PASS','checks':actual['checks'],'new_native_measurements':0,
        'matched_model_comparison':'PASS','new_model_checks':model_actual['checks'],'candidate_centered_anchor_audit':anchor_actual['checks'],'ordersage_secondary_assessment':external,'joint_query_checks':joint_actual['independent_checks'],'calibration_reference':calibration_reference,'explanation_radius_checks':radius_actual['independent_checks'],'partial_ranking_checks':order_actual['independent_checks'],'retained_total_order_queries':order_actual['retained_total_orders']['queries'],'exact_window_partition':exact_actual['classification_counts'],'exact_certificate_sha256':exact_actual['certificate_sha256'],'complete_order_tight_cases':full_actual['cases'],'scalar_archive_pairs':archive_actual['paired_instances'],'scalar_archive_LPs':archive_actual['original_variable_minimum_LPs'],'fixed_ranking_cases':matching_actual['controlled_cases'],'exact_assignment_dual_witnesses':matching_actual['exact_integer_assignment_dual_witnesses'],'fixed_ranking_minimum_LPs':matching_actual['original_variable_minimum_LPs'],'planned_auditor_queries':auditor_actual['all_fixed_budget_queries'],'planned_auditor_unresolved':auditor_actual['unresolved_exact_decisions_preserved'],'quartet_cases':quartet_actual['instances'],'quartet_tests':quartet_actual['quartet_tests'],'full_factor_larger_than_quartet_max_count':quartet_actual['full_factor_larger_than_quartet_max_count'],'quartet_only_queries':quartet_only_actual['fixed_budget_outputs'],'quartet_only_route_sha256':quartet_only_actual['all_routes_sha256'],'quartet_only_uses_full_factors':False,'two_clause_exposition':'PASS','finite_gap_matching_checks':exposition['gap_sanity_checks']['matching_gap_identities'],'drift_bound_calibrated':False,'untouched_policy_test':False,'public_release_performed_by_runner':False}
    (HERE/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
if __name__=='__main__':main()
