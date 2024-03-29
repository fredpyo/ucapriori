'''
Created on Nov 7, 2009

@author: fede
'''

MINIMUMFONTSIZE = 4

def writeCaption( text, bitmap, font=None, margins = (2,2), color=None ):
        """Write the given caption (text) into the bitmap
        using the font (or default if not given) with the
        margins given.  Will try to make sure the text fits
        into the bitmap.
        """
        memory = wx.MemoryDC( )
        font = font or memory.GetFont()
        textLines = string.split( text, '\n' )
        fit = 0
        """
        while not fit:
                totalWidth=0
                totalHeight = 0
                setLines = []
                for line in textLines:
                        if line and line[-1] == '\r':
                                line = line[:-1]
                        width, height = extents = memory.GetTextExtent( line )
                        totalWidth = max( totalWidth,  width )
                        totalHeight = totalHeight + height
                        setLines.append( (line, extents))
                if (
                        totalWidth > (bitmap.GetWidth()- 2*margins[0]) or
                        totalHeight > (bitmap.GetHeight()- 2*margins[0])
                ):
                        size = font.GetPointSize()-1
                        if size < MINIMUMFONTSIZE:
                                fit = 1 # will overdraw!!!
                        else:
                                font.SetPointSize( size )
                                memory.SetFont( font )
                else:
                        fit = 1
        if not setLines:
                return bitmap
        centreX, centreY = (bitmap.GetWidth()/2), (bitmap.GetHeight()/2)
        x, y = centreX-(totalWidth/2), centreY-(totalHeight/2)
        """
        memory.SelectObject( bitmap )
        gc = wx.GraphicsContext.Create(memory)
        x, y = 0, 0
        _setupContext( memory, font, color)
        #for line, (deltaX, deltaY) in setLines:
        #x = centreX - (deltaX/2)
        print wx.TRANSPARENT == memory.GetBackgroundMode()
        memory.SetBackgroundMode(wx.TRANSPARENT)
        #memory.DrawText( "aijfnaijfn", x, y,)
        gc.SetFont(font, "#ffe090")
        gc.DrawText("aosmoasm", 0, 0)
        #y = y + deltaY
        memory.SelectObject( wx.NullBitmap)
        print bitmap
        return bitmap

def _setupContext( memory, font=None, color=None ):
        if font:
                memory.SetFont( font )
        else:
                memory.SetFont( wxNullFont )
        if color:
                memory.SetTextForeground( color )
                
MINIMUMFONTSIZE = 4

def writeCaption( text, bitmap, font=None, margins = (2,2), color=None ):
        """Write the given caption (text) into the bitmap
        using the font (or default if not given) with the
        margins given.  Will try to make sure the text fits
        into the bitmap.
        """
        memory = wx.MemoryDC( )
        font = font or memory.GetFont()
        textLines = string.split( text, '\n' )
        fit = 0
        """
        while not fit:
                totalWidth=0
                totalHeight = 0
                setLines = []
                for line in textLines:
                        if line and line[-1] == '\r':
                                line = line[:-1]
                        width, height = extents = memory.GetTextExtent( line )
                        totalWidth = max( totalWidth,  width )
                        totalHeight = totalHeight + height
                        setLines.append( (line, extents))
                if (
                        totalWidth > (bitmap.GetWidth()- 2*margins[0]) or
                        totalHeight > (bitmap.GetHeight()- 2*margins[0])
                ):
                        size = font.GetPointSize()-1
                        if size < MINIMUMFONTSIZE:
                                fit = 1 # will overdraw!!!
                        else:
                                font.SetPointSize( size )
                                memory.SetFont( font )
                else:
                        fit = 1
        if not setLines:
                return bitmap
        centreX, centreY = (bitmap.GetWidth()/2), (bitmap.GetHeight()/2)
        x, y = centreX-(totalWidth/2), centreY-(totalHeight/2)
        """
        memory.SelectObject( bitmap )
        gc = wx.GraphicsContext.Create(memory)
        x, y = 0, 0
        _setupContext( memory, font, color)
        #for line, (deltaX, deltaY) in setLines:
        #x = centreX - (deltaX/2)
        print wx.TRANSPARENT == memory.GetBackgroundMode()
        memory.SetBackgroundMode(wx.TRANSPARENT)
        #memory.DrawText( "aijfnaijfn", x, y,)
        gc.SetFont(font, "#ffe090")
        gc.DrawText("aosmoasm", 0, 0)
        #y = y + deltaY
        memory.SelectObject( wx.NullBitmap)
        print bitmap
        return bitmap

def _setupContext( memory, font=None, color=None ):
        if font:
                memory.SetFont( font )
        else:
                memory.SetFont( wxNullFont )
        if color:
                memory.SetTextForeground( color )