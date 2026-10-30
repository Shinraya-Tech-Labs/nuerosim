"""Pure UI-facing projection helpers for testable visualization contracts."""
def status_label(status): return {"queued":"Queued","running":"Running","complete":"Complete","failed":"Failed"}.get(status,status.title())
def picker_options(entries): return [{"value":e,"label":str(e).replace('_',' ').title()} for e in entries]
def model_explainer(model): return {"model":model,"title":model.replace('_',' ').title()}
def current_plot(times,current): return [{"time_ms":t,"current":v} for t,v in zip(times,current)]
def channel_chart(times,series): return [{"time_ms":t,**{k:v[i] for k,v in series.items()}} for i,t in enumerate(times)]
def raster_limit(spikes,limit): return list(spikes[:limit])
def firing_rate_chart(times,rates): return list(zip(times,rates))
def arrow_edges(edges): return [{"source":a,"target":b,"directed":True} for a,b in edges]
def refractory_overlay(spikes,refractory): return [{"start_ms":t,"end_ms":t+refractory} for t in spikes]
def stdp_trajectory(times,weights): return list(zip(times,weights))
def morphology_view(vertices,edges): return {"vertices":vertices,"edges":edges}
def compare_runs(runs): return {"run_count":len(runs),"runs":runs}
def comparison_matrix(runs): return [[a.get('label') for a in runs]]
def svg_metadata(width,height,units='px'): return {"width":width,"height":height,"units":units}
def keyboard_order(labels): return list(labels)
def reduced_motion(preference): return bool(preference)
