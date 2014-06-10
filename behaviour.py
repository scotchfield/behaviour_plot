import pygame
from pygame.locals import *

import optparse
import os
import random
import sys

resolution = [ 1200, 400 ]


def add_variable_line( options, line ):
    line = line.strip()

    if line.startswith( '#' ):
        return

    if line.find( '=' ) > -1:
        line_obj = line.split( '=' )
        key = line_obj[ 0 ].strip()
        value = line_obj[ 1 ].strip()
        while value.find( '(' ) > -1:
            var = value[ value.find( '(' ) + 1 : value.find( ')' ) ]
            if var not in options:
                print( 'ERROR: %s used but not defined - skipping' % ( var ) )
                return
            value = '%s%s%s' % (
                value[ : value.find( '(' ) ],
                options.get( var ),
                value[ value.find( ')' ) + 1 : ] )

        options[ key ] = value

def get_configuration( config_file ):
    options = {}

    try:
        input_file = open( config_file, 'r' )
    except IOError:
        return False

    for line in input_file:
        add_variable_line( options, line )

    return options


def draw_lines( screen, n ):
    height = resolution[ 1 ] / float( n + 1 )
    for i in range( 1, n + 1 ):
        y = int( height * i )
        pygame.draw.line( screen, ( 0, 0, 0 ),
                         ( 20, y ), ( resolution[ 0 ] - 20, y ), 4 )

def draw_data( screen, n, colour_obj, data_obj ):
    height = resolution[ 1 ] / float( n + 1 )
    x_mid = round( resolution[ 0 ] / 2 )
    x_radius = x_mid - 20

    for i in range( n ):
        y = int( height * ( i + 1 ) )

        if len( data_obj ) <= i:
            continue

        for j in data_obj[ i ]:
            x = x_mid + round( j * x_radius )
            pygame.draw.rect( screen, colour_obj[ i ],
                              ( x - 5, y - 30, 10, 60 ) )


def draw_events( screen, n, event_colour, event_obj ):
    height = resolution[ 1 ] / float( n + 1 )
    x_mid = round( resolution[ 0 ] / 2 )
    x_radius = x_mid - 20

    for i in range( n ):
        y = int( height * ( i + 1 ) )

        if len( event_obj ) <= i:
            continue

        for j in event_obj[ i ]:
            x = x_mid + round( j * x_radius )
            pygame.draw.rect( screen, ( 0, 0, 0 ),
                              ( x - 9, y - 50, 18, 100 ) )
            pygame.draw.rect( screen, event_colour,
                              ( x - 5, y - 46, 10, 92 ) )


def main():
    parser = optparse.OptionParser( 'usage: %prog [options] arg1 arg2' )
    parser.add_option( '-c', '--config_file', dest = 'config_file',
                       default = '', type = 'string',
                       help = 'configuration file to use' )

    ( options, args ) = parser.parse_args()

    config_options = get_configuration( options.config_file )

    if options.config_file == '':
        print( 'No configuration file given!' )
        sys.exit( 0 );

    colour_obj = []
    for i in range( int( config_options[ 'lines' ] ) ):
        colour = config_options[ 'colour_' + str( i ) ].split( ',' )
        for j in range( len( colour ) ):
            colour[ j ] = int( colour[ j ] )
        colour_obj.append( colour )

    event_colour = config_options[ 'colour_event' ].split( ',' )
    for i in range( len( event_colour ) ):
        event_colour[ i ] = int( event_colour[ i ] )

    data_obj = []
    input_file = open( config_options[ 'data_file' ], 'r' )
    for line in input_file:
        line_obj = line.strip().split( ',' )
        for i in range( len( line_obj ) ):
            line_obj[ i ] = float( line_obj[ i ] )
        data_obj.append( line_obj )
    input_file.close()

    event_obj = []
    input_file = open( config_options[ 'event_file' ], 'r' )
    for line in input_file:
        line_obj = line.strip().split( ',' )
        for i in range( len( line_obj ) ):
            line_obj[ i ] = float( line_obj[ i ] )
        event_obj.append( line_obj )
    input_file.close()

    pygame.init()
    screen = pygame.display.set_mode( resolution )

    done = False
    while not done:
        screen.fill( ( 255, 255, 255 ) )
        draw_lines( screen, int( config_options[ 'lines' ] ) )
        draw_data( screen, int( config_options[ 'lines' ] ),
                   colour_obj, data_obj )
        draw_events( screen, int( config_options[ 'lines' ] ),
                     event_colour, event_obj )
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE) or (e.type == KEYUP and e.key == 113):
                done = True
            elif e.type == KEYUP and e.key == K_RETURN:
                pygame.image.save( screen, '{0}{1}.png'.format(
                    output_folder, user_index ) )


if __name__ == "__main__":
    main()
