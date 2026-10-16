const sports = ['baseball','ice-hockey','american-football','football','tennis','basketball'];
const object = properties => ({type:'object',properties,additionalProperties:false});
const integer = {type:'integer',minimum:1};
const annotations = {readOnlyHint:true,destructiveHint:false,idempotentHint:true,openWorldHint:true};
export const tools = [
 {name:'sofascore_schedule',description:'Read scheduled matches by sport and date from unofficial SofaScore endpoints. Returns source and fetch time. A provider refusal is an error, never an empty schedule.',inputSchema:{...object({sport:{type:'string',enum:sports},date:{type:'string',pattern:'^\\d{4}-\\d{2}-\\d{2}$'}}),required:['sport','date']},annotations},
 {name:'sofascore_history',description:'Read one page of a verified team or player historical matches. Does not assert all matches are completed; check status and score settlement.',inputSchema:{...object({kind:{type:'string',enum:['team','player']},id:integer,page:{type:'integer',minimum:0,maximum:5}}),required:['kind','id']},annotations},
 {name:'sofascore_statistics',description:'Read statistics by period for a verified SofaScore event ID. Check available fields and period before calculating any market; missing values are not zero.',inputSchema:{...object({event_id:integer}),required:['event_id']},annotations},
 {name:'historical_threshold',description:'Calculate L5/L10/L20/L30 historical over/under frequency from explicitly mapped observations of ONE exact market, period and settlement. Not a prediction. Filter surface/home/away/opponent before calling. Deduplicates IDs; excludes future and unfinished events; missing observations remain visible.',inputSchema:{...object({event_key:{type:'string',minLength:1},line:{type:'number'},direction:{type:'string',enum:['over','under']},as_of:{type:'string',format:'date-time'},window:{type:'integer',enum:[5,10,20,30]},rows:{type:'array',maxItems:200,items:{...object({event_id:integer,start_utc:{type:'string',format:'date-time'},status:{type:'string'},value:{type:['number','null']},source:{type:'string',minLength:1}}),required:['event_id','start_utc','status','value','source']}}}),required:['event_key','line','direction','as_of','window','rows']},annotations:{...annotations,openWorldHint:false}}
];
function requireValue(condition,message){if(!condition) throw new Error(message);}
function date(value){requireValue(typeof value==='string' && /(Z|[+-]\d\d:\d\d)$/.test(value),'Timezone required');const d=Date.parse(value);requireValue(Number.isFinite(d),'Invalid timestamp');return d;}
export function frequency(a){
 requireValue(typeof a.event_key==='string'&&a.event_key.trim()&&Number.isFinite(a.line)&&['over','under'].includes(a.direction)&&[5,10,20,30].includes(a.window)&&Array.isArray(a.rows)&&a.rows.length<=200,'Invalid frequency arguments');
 const cutoff=date(a.as_of), seen=new Map();
 for(const row of a.rows){
  requireValue(Number.isInteger(row.event_id)&&row.event_id>0&&typeof row.source==='string'&&row.source.length>0,'Event ID and provenance required');
  const start=date(row.start_utc);
  if(row.status!=='completed'||start>=cutoff)continue;
  requireValue(row.value===null||(typeof row.value==='number'&&Number.isFinite(row.value)),'Value must be numeric or null');
  requireValue(!seen.has(row.event_id)||JSON.stringify(seen.get(row.event_id))===JSON.stringify(row),'Conflicting duplicate event');seen.set(row.event_id,row);
 }
 const recent=[...seen.values()].sort((a,b)=>date(b.start_utc)-date(a.start_utc)).slice(0,a.window);
 const gamelog=recent.map(r=>({...r,outcome:r.value===null?'missing':r.value===a.line?'push':((r.value>a.line)===(a.direction==='over'))?'win':'loss'}));
 const count=outcome=>gamelog.filter(r=>r.outcome===outcome).length;
 const observed=recent.length-count('missing');
 return {event_key:a.event_key,line:a.line,direction:a.direction,as_of:a.as_of,window:a.window,games_in_window:recent.length,observed,wins:count('win'),losses:count('loss'),pushes:count('push'),missing:count('missing'),observed_hit_rate:observed?count('win')/observed:null,gamelog,interpretation:'Historical frequency only; not future probability. Pushes are included in observed denominator. No automatic stat mapping.'};
}
async function source(path){
 const url='https://www.sofascore.com/api/v1/'+path;
 const response=await fetch(url,{headers:{Accept:'application/json'},redirect:'error',signal:AbortSignal.timeout(15000)});
 if(!response.ok)throw new Error('SofaScore HTTP '+response.status+'. No data returned; do not treat as zero or retry to bypass refusal.');
 const data=await response.json();
 return {source:url,fetched_at:new Date().toISOString(),unofficial:true,data};
}
export async function runTool(name,a){
 if(name==='historical_threshold')return frequency(a);
 if(name==='sofascore_schedule'){
  requireValue(sports.includes(a.sport)&&typeof a.date==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(a.date)&&new Date(a.date).toISOString().slice(0,10)===a.date,'Invalid sport/date');
  return source('sport/'+a.sport+'/scheduled-events/'+a.date);
 }
 if(name==='sofascore_history'){
  const page=a.page??0;
  requireValue(['team','player'].includes(a.kind)&&Number.isInteger(a.id)&&a.id>0&&Number.isInteger(page)&&page>=0&&page<=5,'Invalid history arguments');
  return source(a.kind+'/'+a.id+'/events/last/'+page);
 }
 if(name==='sofascore_statistics'){
  requireValue(Number.isInteger(a.event_id)&&a.event_id>0,'Invalid event ID');return source('event/'+a.event_id+'/statistics');
 }
 throw new Error('Unknown tool');
}
const json=value=>Response.json(value);
export default {async fetch(request){
 if(new URL(request.url).pathname!=='/mcp')return new Response(`<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>SportLab SofaScore</title><style>body{font:17px system-ui;background:#101827;color:#edf2ff;max-width:740px;margin:70px auto;padding:24px}h1{color:#6ce5bd}li{margin:15px 0}p{line-height:1.7}a{color:#6ce5bd}</style><h1>SportLab SofaScore</h1><p>Plugin privado de investigación deportiva. Integración no oficial.</p><ul><li>Consultar calendarios de seis deportes.</li><li>Consultar históricos de equipos y jugadores.</li><li>Leer estadísticas por partido y período.</li><li>Calcular frecuencias históricas L5/L10/L20/L30.</li></ul><p>Los datos dependen de la disponibilidad y permisos de SofaScore. Una respuesta 403 significa acceso rechazado; no significa que no existan partidos. El cálculo de tendencias recibe observaciones con fuente y no transforma frecuencias en probabilidades futuras.</p><p>Herramientas disponibles mediante MCP en <code>/mcp</code>.</p><p><a href="https://github.com/Gianlouis47/Sportlab-Universal">Repositorio SportLab</a></p></html>`,{headers:{'Content-Type':'text/html;charset=utf-8'}});
 if(request.method!=='POST')return new Response('POST required',{status:405});
 let rpc;try{rpc=await request.json();}catch{return json({jsonrpc:'2.0',id:null,error:{code:-32700,message:'Invalid JSON'}});}
 const base={jsonrpc:'2.0',id:rpc.id??null};
 if(rpc.method==='server/discover')return json({...base,result:{supportedVersions:['2026-07-28'],capabilities:{tools:{}}}});
 if(rpc.method==='initialize')return json({...base,result:{protocolVersion:'2025-03-26',capabilities:{tools:{}},serverInfo:{name:'sportlab-sofascore',version:'1.0.0'}}});
 if(rpc.method==='notifications/initialized')return new Response(null,{status:202});
 if(rpc.method==='tools/list')return json({...base,result:{tools}});
 if(rpc.method==='tools/call'){
  try{const result=await runTool(rpc.params?.name,rpc.params?.arguments??{});return json({...base,result:{content:[{type:'text',text:JSON.stringify(result)}]}});}
  catch(e){return json({...base,result:{isError:true,content:[{type:'text',text:e.message}]}});}
 }
 return json({...base,error:{code:-32601,message:'Unknown method'}});
}};
