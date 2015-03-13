# OpenRTS - Copyright (C) 2006 The OpenRTS Project
#
# OpenRTS is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# OpenRTS is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

import pygame
from pygame.locals import *
import string
import sys, os, os.path
import logging
import Image
import JpegImagePlugin
import PngImagePlugin
import BmpImagePlugin
import GifImagePlugin 
import TgaImagePlugin 



from xml.dom import minidom, Node

#****************************************************************************
# The tileset class reads tileset information from a XML file, and 
# loads the corresponding graphics files into pygame surfaces.
#****************************************************************************
class Tileset:
  def __init__(self, clientstate):
    self.client = clientstate;

    self.imagestore = {}  # Stores Pygame surfaces
    self.animstore = {}   # Stores the number of animation frames
    self.animation_frame = 0;


#****************************************************************************
#
#****************************************************************************
  def load_tileset(self):
    self.imagestore = None 
    self.imagestore = {}
    self.edges = {};
    tilesetfile = self.client.settings.tileset;
    doc = minidom.parse(tilesetfile);
    rootNode = doc.documentElement;
    tilesetPath = rootNode.getAttribute('path');
    self.tile_width = int(rootNode.getAttribute('tile_width'));
    self.tile_height = int(rootNode.getAttribute('tile_height'));
    self.edge_tile_height = int(rootNode.getAttribute('edge_tile_height'));
    self.panel_width = int(rootNode.getAttribute('panel_width'));
    self.panel_height = int(rootNode.getAttribute('panel_height'));

    for fileNode in rootNode.getElementsByTagName('file'):
      image_file_name = os.path.join(tilesetPath, fileNode.getAttribute('src'));
      try:
        #  Load image file with PIL.
        image_full = Image.open(image_file_name);
      except IOError:
        logging.error("Loading of graphic file failed: %s" % (image_file_name));
        pygame.quit();

      # Load any sprite at a specified position
      for tileNode in fileNode.getElementsByTagName('sprite'):
        name = tileNode.getAttribute('name'); 
        x = int(tileNode.getAttribute('x'));
        y = int(tileNode.getAttribute('y'));
        width = int(tileNode.getAttribute('width'));
        height = int(tileNode.getAttribute('height'));
        per_pixel_alpha = ("true" == str(tileNode.getAttribute('pixelalpha')));
        self.tileset_add_image(image_full, name, x, y, width, height, per_pixel_alpha);


      # Load a terrain tile 
      for tileNode in fileNode.getElementsByTagName('terrain'):
        name = tileNode.getAttribute('name'); 
        x = int(tileNode.getAttribute('x'));
        y = int(tileNode.getAttribute('y'));
        width = int(tileNode.getAttribute('width'));
        height = int(tileNode.getAttribute('height'));
        per_pixel_alpha = ("true" == str(tileNode.getAttribute('pixelalpha')));

        for frameNode in tileNode.getElementsByTagName('frame'):
          slotx = int(frameNode.getAttribute('slot-x'));
          sloty = int(frameNode.getAttribute('slot-y'));
          sub_x = x + slotx * width + slotx;
          sub_y = y + sloty * height + sloty;
          self.tileset_add_image(image_full, name, sub_x, sub_y, width, height, per_pixel_alpha);

      # Load a edge tile 
      for tileNode in fileNode.getElementsByTagName('edgeterrain'):
        primary = tileNode.getAttribute('primary'); 
        secondary = tileNode.getAttribute('secondary'); 
        self.edges.update({primary:secondary});
        x = int(tileNode.getAttribute('x'));
        y = int(tileNode.getAttribute('y'));
        width = int(tileNode.getAttribute('width'));
        height = int(tileNode.getAttribute('height'));
        per_pixel_alpha = ("true" == str(tileNode.getAttribute('pixelalpha')));

        for frameNode in tileNode.getElementsByTagName('frame'):
          slotx = int(frameNode.getAttribute('slot-x'));
          sloty = int(frameNode.getAttribute('slot-y'));
          edge_key = frameNode.getAttribute('key'); 
          key = primary + "-" + secondary + "-" + edge_key;
          sub_x = x + slotx * width + slotx;
          sub_y = y + sloty * height + sloty;
          self.tileset_add_image(image_full, key, sub_x, sub_y, width, height, per_pixel_alpha);

      # Load units graphic
      for tileNode in fileNode.getElementsByTagName('unit'):
        name = tileNode.getAttribute('name'); 
        x = int(tileNode.getAttribute('x'));
        y = int(tileNode.getAttribute('y'));
        frames = int(tileNode.getAttribute('frames'));
        width = int(tileNode.getAttribute('width'));
        height = int(tileNode.getAttribute('height'));
        per_pixel_alpha = ("true" == str(tileNode.getAttribute('pixelalpha')));
        self.animstore.update({name: frames});

        for frameNode in tileNode.getElementsByTagName('frame'):
          slotx = int(frameNode.getAttribute('slot-x'));
          sloty = int(frameNode.getAttribute('slot-y'));
          dir = frameNode.getAttribute('dir');
          frame = frameNode.getAttribute('anim_frame');
          key = name + dir + frame;
          sub_x = x + slotx * width + slotx;
          sub_y = y + sloty * height + sloty;
          self.tileset_add_image(image_full, key, sub_x, 
                                 sub_y, width, height, per_pixel_alpha, (255,10,10));

      # Load bullet graphic
      for tileNode in fileNode.getElementsByTagName('bullet'):
        name = tileNode.getAttribute('name'); 
        x = int(tileNode.getAttribute('x'));
        y = int(tileNode.getAttribute('y'));
        frames = int(tileNode.getAttribute('frames'));
        width = int(tileNode.getAttribute('width'));
        height = int(tileNode.getAttribute('height'));
        per_pixel_alpha = ("true" == str(tileNode.getAttribute('pixelalpha')));
        self.animstore.update({name: frames});

        for frameNode in tileNode.getElementsByTagName('frame'):
          slotx = int(frameNode.getAttribute('slot-x'));
          sloty = int(frameNode.getAttribute('slot-y'));
          dir = frameNode.getAttribute('dir');
          frame = frameNode.getAttribute('anim_frame');
          key = name + dir + frame;
          sub_x = x + slotx * width + slotx;
          sub_y = y + sloty * height + sloty;
          self.tileset_add_image(image_full, key, sub_x, 
                                 sub_y, width, height, per_pixel_alpha, (255,10,10));


    # Load mouse cursors
      for tileNode in fileNode.getElementsByTagName('cursor'):
        name = tileNode.getAttribute('name'); 
        x = int(tileNode.getAttribute('x'));
        y = int(tileNode.getAttribute('y'));
        frames = int(tileNode.getAttribute('frames'));
        width = int(tileNode.getAttribute('width'));
        height = int(tileNode.getAttribute('height'));
        per_pixel_alpha = ("true" == str(tileNode.getAttribute('pixelalpha')));
        self.animstore.update({name: frames});

        for frameNode in tileNode.getElementsByTagName('frame'):
          slotx = int(frameNode.getAttribute('slot-x'));
          sloty = int(frameNode.getAttribute('slot-y'));
          frame = frameNode.getAttribute('anim_frame');
          key = name + frame;
          sub_x = x + slotx * width + slotx;
          sub_y = y + sloty * height + sloty;
          self.tileset_add_image(image_full, key, sub_x, 
                                 sub_y, width, height, per_pixel_alpha);


#****************************************************************************
#
#****************************************************************************
  def tileset_add_image(self, image, key, x, y, width, height, alpha, color=None):
        #  Crop tile from image.
        image = image.crop((x, y, x + width, y + height));

        if color:
          data_orig = image.getdata();
          data_color = [];
          for pixel in data_orig:
            (red, green, blue, a) = pixel;
            (new_r, new_g, new_b) = color;
            if (red < blue + 10 and red > blue - 10 and green < 60):
              new_color = (red * new_r / 255, new_g * red / 255, new_b * red / 255, a);
              data_color.append(new_color);
            else:
              data_color.append(pixel);
          image.putdata(data_color); 

        #  Create Pygame surface from PIL image. 
        surface = pygame.image.fromstring(image.tostring(), image.size, image.mode);
        image = None;

        #  If not per pixel alpha (slow), then use a colorkey.
        if not alpha:
          colorkey = surface.get_at((0,0));
          surface.set_colorkey(colorkey, RLEACCEL);

        result = surface.convert_alpha();

        self.imagestore.update({key: result});

#****************************************************************************
#
#****************************************************************************
  def get_terrain_surf_from_tile(self, tile):
    tile_key = str(tile.type.id);
    try:
      return self.imagestore[tile_key];
    except KeyError:
      return None;

#****************************************************************************
#
#****************************************************************************
  def is_edge_tile(self, tile):
    is_edge = 0;
    for adj_tile in self.client.map.get_adjacent_tiles((tile.x, tile.y)):
      if tile.type.id != adj_tile.type.id:
        is_edge = 1;

    return (is_edge and str(tile.type.id) in self.edges);

#****************************************************************************
#
#****************************************************************************
  def get_edge_surf_from_tile(self, tile):
    real_map_x = tile.x;
    real_map_y = tile.y;

    for adj_tile in self.client.map.get_adjacent_tiles((tile.x, tile.y)):
      if tile.type.id != adj_tile.type.id:
        secondary_type = str(adj_tile.type.id);

    nw = self.client.map.get_north_west_tile((real_map_x, real_map_y)); 
    ne = self.client.map.get_north_east_tile((real_map_x, real_map_y)); 
    sw = self.client.map.get_south_west_tile((real_map_x, real_map_y)); 
    se = self.client.map.get_south_east_tile((real_map_x, real_map_y)); 
    n = self.client.map.get_north_tile((real_map_x, real_map_y)); 
    w = self.client.map.get_west_tile((real_map_x, real_map_y)); 
    e = self.client.map.get_east_tile((real_map_x, real_map_y)); 
    s = self.client.map.get_south_tile((real_map_x, real_map_y)); 
    if (not nw or not ne or not sw or not se): return;
    coast_str_1 = ("%s%su%s" % 
             (self.client.map.get_coast_type(nw), 
              self.client.map.get_coast_type(n),
              self.client.map.get_coast_type(w)));
    coast_str_2 = ("%s%s%su" % 
             (self.client.map.get_coast_type(n), 
              self.client.map.get_coast_type(ne),
              self.client.map.get_coast_type(e)));

    coast_str_3 = ("u%s%s%s" % 
             (self.client.map.get_coast_type(e), 
              self.client.map.get_coast_type(se),
              self.client.map.get_coast_type(s)));

    coast_str_4 = ("%su%s%s" % 
             (self.client.map.get_coast_type(w), 
              self.client.map.get_coast_type(s),
              self.client.map.get_coast_type(sw)));

    tile_key1 = ("%s-%s-%s" % (tile.type.id, secondary_type, coast_str_1));
    tile_key2 = ("%s-%s-%s" % (tile.type.id, secondary_type, coast_str_2));
    tile_key3 = ("%s-%s-%s" % (tile.type.id, secondary_type, coast_str_3));
    tile_key4 = ("%s-%s-%s" % (tile.type.id, secondary_type, coast_str_4));

    surface1 = self.imagestore[tile_key1];
    surface2 = self.imagestore[tile_key2];
    surface3 = self.imagestore[tile_key3];
    surface4 = self.imagestore[tile_key4];

    return (surface1, surface2, surface3, surface4);


#****************************************************************************
#
#****************************************************************************
  def get_tile_surf(self, key, height=None):
    try:
      return self.imagestore[key];
    except KeyError:
      return None;

#****************************************************************************
#
#****************************************************************************
  def get_unit_surf_from_tile(self, unit_sprite, dir):
    frames_max = self.animstore[unit_sprite];
    frame = int(self.animation_frame) % frames_max;
    tile_key = "%s%s%r" % (unit_sprite, dir, frame);
    try:
      return self.imagestore[tile_key];
    except KeyError:
      return None;

#****************************************************************************
#
#****************************************************************************
  def get_mouse_cursor(self, type):
    frames_max = self.animstore[type];
    frame = int(self.animation_frame) % frames_max;
    tile_key = "%s%r" % (type, frame);
    try:
      return self.imagestore[tile_key];
    except KeyError:
      return None;

#****************************************************************************
#
#****************************************************************************
  def animation_next(self):
    self.animation_frame += 0.5;

#****************************************************************************
# This method returns a pygame surface from a filename.
#****************************************************************************
def load(image_file_name):
  try:
    # Load image file with PIL.
    image = Image.open(image_file_name);
    # Convert PIL image to Pygame surface
    return pygame.image.fromstring(image.tostring(), image.size, image.mode);

  except IOError:
    logging.error("Loading of graphic file failed: %s" % (image_file_name));
    pygame.quit();



