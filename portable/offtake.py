"""Local monthly off-take: configuration, validation and output copies only."""
from __future__ import annotations
import argparse,hashlib,html,json,os,sys,zipfile
from pathlib import Path
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
for folder in [ROOT/'automation',ROOT/'engine/Automacao off-take']:
 if str(folder) not in sys.path:sys.path.insert(0,str(folder))

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def write(path,value):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def require(ok,message):
 if not ok:raise ValueError(message)
def private_path(value):
 p=(ROOT/value).resolve()
 require(p.is_relative_to(ROOT) and p!=ROOT,'Configuration path must remain inside this installation.')
 return p

def verify_distribution():
 manifest=ROOT/'DISTRIBUTION_MANIFEST.json'
 require(manifest.is_file(),'Distribution manifest is missing. Extract the complete private company package.')
 doc=read(manifest)
 for row in doc['immutable_files']:
  p=private_path(row['path'])
  require(p.is_file() and not p.is_symlink() and sha(p)==row['sha256'],'Distribution file changed or missing: '+row['path'])
 return {'checked':len(doc['immutable_files']),'passed':True,'manifest_sha256':sha(manifest)}

def configure():
 require(os.name!='nt' or len(str(ROOT))<=60,'Extract this package to a short folder, such as %USERPROFILE%\\AlchemyOfftake, then run INSTALL.cmd there (installation path limit: 60 characters). This avoids Windows long-path failures without changing system settings.')
 check=verify_distribution()
 config=read(ROOT/'company/company.json')
 archive=private_path(config['templates_archive'])
 catalogue=private_path(config['identity_catalogue'])
 require(sha(archive)==config['templates_sha256'],'Company template archive does not match its reviewed configuration.')
 require(sha(catalogue)==config['catalogue_sha256'],'Company identity catalogue changed. Review it before configuring.')
 import template_base
 imported=template_base.import_base(archive,closed_through=config['closed_through'])
 manifest=Path(imported['manifest']);doc=template_base.verify_manifest(manifest)
 require(doc['counts']['xlsx']==config['template_count'] and doc['counts']['outlets']==config['outlet_template_count'],'Company template counts differ from the reviewed package.')
 with zipfile.ZipFile(archive) as z:require(z.testzip() is None,'Template archive failed its CRC check.')
 audit_path=ROOT/'configuration/template-audit.json'
 # Retain activation/audit history when reconfiguring after relocation.
 for prior in [audit_path,ROOT/'automation/template-base.json']:
  if prior.is_file():
   history=ROOT/'configuration/history'/(prior.stem+'-'+sha(prior)+'.json')
   history.parent.mkdir(parents=True,exist_ok=True)
   if not history.exists():history.write_bytes(prior.read_bytes())
 audit={'status':'PASSED','kind':'portable_installation_template_copy_audit','created_at':datetime.now(timezone.utc).isoformat(),'extraction_manifest':{'path':str(manifest.resolve()),'sha256':sha(manifest)},'source_zip_sha256':sha(archive),'archive':{'sha256_before':sha(archive),'sha256_after':sha(archive),'crc_all_members_passed':True},'summary':{'extracted_workbooks_hashes_match_all_zip_members':True,'extracted_workbooks_unchanged_during_audit':True},'scope':'Verified the bundled reviewed archive, exact extracted bytes, workbook inventory, native package CRC and monthly structure. This is installation verification, not new finance approval.','distribution':check}
 write(audit_path,audit)
 active=template_base.activate(imported,audit_path=audit_path)
 for name in ['protected-inputs','reports','output']:(ROOT/name).mkdir(exist_ok=True)
 result={'status':'CONFIGURED','closed_through':active['closed_through'],'next_period':template_base.next_period(active),'templates':active['counts'],'catalogue_records':config['identity_records'],'company_wide_readiness':False,'financial_publication':False,'scheduling':False}
 write(ROOT/'configuration/installation.json',result)
 return result

def doctor():
 result={'distribution':verify_distribution(),'platform':sys.platform,'python':sys.version.split()[0],'no_codex_required':True,'network_used':False,'financial_publication':False}
 require(sys.version_info>=(3,12),'Python 3.12 or later is required.')
 import importlib.metadata as metadata
 result['libraries']={n:metadata.version(n) for n in ['openpyxl','pdfplumber','tzdata']}
 from zoneinfo import ZoneInfo
 require(ZoneInfo('Asia/Bangkok') is not None,'Bangkok time zone data is unavailable.')
 try:
  import template_base
  active=template_base.get_active()
  result['templates']={'status':'configured','counts':active['counts'],'closed_through':active['closed_through']}
 except (ValueError,FileNotFoundError) as exc:result['templates']={'status':'NOT_CONFIGURED','action':'Run INSTALL.cmd in this folder.','detail':str(exc)}
 return result

def generate(period,reports,validate_only=False):
 require(os.name!='nt' or len(str(ROOT))<=60,'Move/extract the full package to %USERPROFILE%\\AlchemyOfftake and run INSTALL.cmd again. The installation path must be at most 60 characters.')
 verify_distribution()
 config=read(ROOT/'company/company.json')
 import run_monthly
 report_path=Path(reports).expanduser().resolve(strict=True)
 require(report_path.is_dir(),'Select a folder of actual monthly reports.')
 # Historical references and outputs are never monthly input reports.
 forbidden=[ROOT/'company',ROOT/'engine',ROOT/'template-bases',ROOT/'runtime',ROOT/'automation',ROOT/'output']
 require(not any(report_path.is_relative_to(p.resolve()) or p.resolve().is_relative_to(report_path) for p in forbidden),'Reports must be separate from the program, company references, templates and previous results.')
 result=run_monthly.execute(period,report_path,validate_only=validate_only,progress=lambda _:None)
 statuses={'GERADO':'GENERATED','PARCIAL_GERADO':'PARTIAL_COPIES_GENERATED','VALIDADO_SEM_GERAR':'VALIDATED_NO_WORKBOOKS_WRITTEN','VALIDADO_PARCIAL_SEM_GERAR':'PARTIAL_VALIDATION_NO_WORKBOOKS_WRITTEN','PENDENTE':'NEEDS_REVIEW','FALHOU':'FAILED','ENTRADAS_ALTERADAS':'INPUTS_CHANGED'}
 status=statuses.get(result['status'],result['status'])
 job=Path(result['job'])
 details={'status':status,'period':period,'generated_workbooks':result.get('output_count',0),'closing_complete':result.get('closing_complete',False),'result_folder':str(job),'financial_publication':False,'company_wide_readiness':False,'engine_receipt':'recibo.json','issues':result.get('issues',[]),'input_integrity':result.get('input_integrity'),'calculation_backend':'reviewed_python_formula_model','independent_second_formula_engine':False,'source_rule':'Actual current reports; historical files never create sales or zero evidence.'}
 write(job/'RESULT.json',details)
 links=''.join('<li><a href="'+html.escape(d['path'],quote=True)+'">'+html.escape(d['path'])+'</a></li>' for d in result.get('deliverables',[]))
 page='<!doctype html><html lang="en"><meta charset="utf-8"><title>Monthly off-take</title><style>body{font:17px system-ui;max-width:850px;margin:45px auto;padding:20px}a{color:#096949}</style><h1>Monthly off-take '+html.escape(period)+'</h1><h2>'+status+'</h2><p>'+str(details['generated_workbooks'])+' outlet workbook copies generated. Originals have not been installed or overwritten.</p><p>Partial results do not close the month. Missing reports or accounts remain pending and never become zero sales.</p><ul>'+links+'</ul><p><a href="PENDENCIAS.csv">Review pending issues</a> · <a href="RESULT.json">English execution summary</a></p><p>Some legacy diagnostic messages remain in Portuguese. Unsupported layouts, uncertain accounts/SKUs, periods, units or VAT block the affected run or outlet.</p></html>'
 (job/'RESULT.html').write_text(page,encoding='utf-8')
 details['result']=str(job/'RESULT.html')
 return details

def interactive():
 print('ALCHEMY MONTHLY OFF-TAKE — local workbook copies only\n')
 try:
  import template_base
  active=template_base.get_active();default=template_base.next_period(active)
 except (ValueError,FileNotFoundError):
  print('Run INSTALL.cmd first.');return 2
 period=input('Month YYYY-MM ['+default+']: ').strip() or default
 reports=input('Paste the folder containing the monthly reports: ').strip().strip('"')
 print('Reading reports, generating copies and validating. Please wait...')
 result=generate(period,reports)
 print(json.dumps({k:v for k,v in result.items() if k not in ['issues']},indent=2))
 if os.name=='nt':os.startfile(result['result'])
 return 0 if result['status'] in ['GENERATED','PARTIAL_COPIES_GENERATED'] else 2

def main(argv=None):
 parser=argparse.ArgumentParser(description=__doc__)
 sub=parser.add_subparsers(dest='command')
 sub.add_parser('configure');sub.add_parser('doctor')
 run=sub.add_parser('run');run.add_argument('--period',required=True);run.add_argument('--reports',required=True);run.add_argument('--validate-only',action='store_true')
 args=parser.parse_args(argv)
 if args.command is None:return interactive()
 if args.command=='configure':result=configure()
 elif args.command=='doctor':result=doctor()
 else:result=generate(args.period,args.reports,args.validate_only)
 print(json.dumps(result,ensure_ascii=False,indent=2))
 if args.command=='run' and result['status'] not in ['GENERATED','PARTIAL_COPIES_GENERATED','VALIDATED_NO_WORKBOOKS_WRITTEN','PARTIAL_VALIDATION_NO_WORKBOOKS_WRITTEN']:return 2
 return 0

if __name__=='__main__':
 try:raise SystemExit(main())
 except Exception as exc:
  print('Off-take stopped safely: '+str(exc),file=sys.stderr);raise SystemExit(2)
