from random import random
from manim import *
class CreationDestructionMobject(VMobject):
  CONFIG={
    'start_time':0,
    'frequency':0.1,
    'max_ratio_shown':0.1,
    'use_copy':False,
  }
  def __init__(self,template,**kwargs):
    VMobject.__init__(self,kwargs)
    if self.CONFIG['use_copy']:
      self.ghost_mob=template.copy().fade(1)
      self.add(self.ghost_mob)
    else:
      self.ghost_mob=template
    self.shown_mob=template.copy()
    self.shown_mob.clear_updaters()
    self.add(self.shown_mob)
    self.total_time=self.CONFIG['start_time']
    def update(mob,dt):
      mob.total_time+=dt
      period=1/mob.CONFIG['frequency']
      unsmooth_alpha=(mob.total_time%period)/period
      alpha=bezier([dt%1,1,0,0])(unsmooth_alpha)
      mob.shown_mob.pointwise_become_partial(
        mob.ghost_mob,
        max(interpolate(-mob.CONFIG['max_ratio_shown'],1,alpha),0),
        min(interpolate(0,1+mob.CONFIG['max_ratio_shown'],alpha),1)
      )
    self.add_updater(update)
class Eddy(VMobject):
  CONFIG={
    'n_layers':20,
    'frequency':0.2,
  }
  def __init__(self,**kwargs):
    VMobject.__init__(self,*kwargs)
    lines=self.get_lines()
    self.add(*[
      CreationDestructionMobject(line)
      for line in lines
    ])
    self.randomize_times()
  def get_lines(self):
    lines=VGroup(*[
      ParametricFunction(
        lambda t: (1+r)*np.array([
          np.cos(TAU*t),
          np.sin(TAU*t),
          0
        ]),
        t_range=np.array([np.random.random(),TAU*np.random.random()]),
        color=interpolate_color(BLUE,RED,np.random.random()),
        stroke_width=np.random.random()*5
      ) for _,r in zip(range(self.CONFIG['n_layers']),np.random.random(size=self.CONFIG['n_layers']))
    ])
    return lines
  def randomize_times(self):
    for submob in self.submobjects:
      if hasattr(submob,'total_time'):
        T=1/submob.CONFIG['frequency']
        submob.total_time=T*np.random.random()
      # else:
      #   T=1
      #   submob.total_time=T*np.random.random()
class Importacion(Scene):
  def construct(self):
    suceso=Eddy()
    self.add(suceso)
    self.wait(4)