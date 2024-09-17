# --- Deslizator - Javier Ramos Jimeno --- #

import time
import wx
from wx.core import GetDisplaySize

#Variables Globales
columnas = 10
filas = [12,0]
lista_filas = []
detector_movimiento = [0,0]
indice = [0]
puntos_partida = [0]
entrada = [0]
CH_PANT = ord('#')
CH_FICH = ord('A')
CH_FIL = ord('A')
CH_COL = ord('0') 

def ciclo(lis):
    while True:
        for elem in lis:
            yield elem
			
class Bloque(object):
    def __init__(self, fil, col0, col1, val):
        self.fila = fil
        self.col0 = col0
        self.col1 = col1
        self.val = val            
        self.ancho = col1 - col0 + 1

    def desplazar(self, dx, dy):
        self.fila += dy
        self.col0 += dx
        self.col1 += dx

class Tablero(object):
    def __init__(self, nomfich, numfil):
        with open(nomfich) as fich:
            entrada[0] = ciclo(fich.read().splitlines())
        self.nfil = numfil
        self.ncol = 10

        datos = [[] for _ in range(numfil)]
   
class Deslizator(wx.App):
	def OnInit(self):
		self.Deslizator = Ventana(None, wx.ID_ANY, "")
		self.SetTopWindow(self.Deslizator)
		self.Deslizator.Centre()
		self.Deslizator.Show()
		return True
		
class Ventana(wx.Frame):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		self.SetMinSize((775, 700))
		self.Centre()
		self.SetTitle("Deslizator - Javier Ramos Jimeno")
		_icon = wx.NullIcon
		_icon.CopyFromBitmap(wx.Bitmap("JavierRamosJimeno_Logo.png", wx.BITMAP_TYPE_ANY))
		self.SetIcon(_icon)

		Separador_Base = wx.BoxSizer(wx.HORIZONTAL)

		Separador_Menu = wx.BoxSizer(wx.VERTICAL)
		Separador_Base.Add(Separador_Menu, 0, wx.ALL | wx.EXPAND, 0)

		Separador_Imagenes = wx.BoxSizer(wx.HORIZONTAL)
		Separador_Menu.Add(Separador_Imagenes, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 0)

		Sizer_Botonabrirfichero = wx.BoxSizer(wx.VERTICAL)
		Separador_Imagenes.Add(Sizer_Botonabrirfichero, 0, wx.EXPAND, 0)

		self.Abrir_Fichero_Image = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("JavierRamosJimeno_AF.png", wx.BITMAP_TYPE_ANY))
		self.Abrir_Fichero_Image.SetSize(self.Abrir_Fichero_Image.GetBestSize())
		Sizer_Botonabrirfichero.Add(self.Abrir_Fichero_Image, 0, 0, 0)

		Sizer_Botonnuevapartida = wx.GridSizer(1, 1, 0, 0)
		Separador_Imagenes.Add(Sizer_Botonnuevapartida, 1, wx.EXPAND, 0)

		self.Nueva_Partida_Image = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("JavierRamosJimeno_EP.png", wx.BITMAP_TYPE_ANY))
		self.Nueva_Partida_Image.SetSize(self.Nueva_Partida_Image.GetBestSize())
		Sizer_Botonnuevapartida.Add(self.Nueva_Partida_Image, 0, 0, 0)

		Sizer_Botonnumerofilas = wx.GridSizer(1, 1, 0, 0)
		Separador_Imagenes.Add(Sizer_Botonnumerofilas, 1, wx.EXPAND, 0)

		self.Grid_Image = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("JavierRamosJimeno_Cuadricula.png", wx.BITMAP_TYPE_ANY))
		self.Grid_Image.SetSize(self.Grid_Image.GetBestSize())
		Sizer_Botonnumerofilas.Add(self.Grid_Image, 0, 0, 0)

		Separador_Puntuacion = wx.BoxSizer(wx.HORIZONTAL)
		Separador_Menu.Add(Separador_Puntuacion, 0, wx.ALL, 5)

		Etiqueta_Puntuacion = wx.StaticText(self, wx.ID_ANY, u"Puntuación:")
		Etiqueta_Puntuacion.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
		Separador_Puntuacion.Add(Etiqueta_Puntuacion, 0, wx.ALIGN_CENTER_VERTICAL | wx.UP, 5)

		self.Puntos = wx.StaticText(self, wx.ID_ANY, str(puntos_partida[0]))
		self.Puntos.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
		Separador_Puntuacion.Add(self.Puntos, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)

		Separador_Jugadas = wx.BoxSizer(wx.VERTICAL)
		Separador_Menu.Add(Separador_Jugadas, 1, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

		Etiqueta_Jugadas = wx.StaticText(self, wx.ID_ANY, "Lista de Jugadas:")
		Etiqueta_Jugadas.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
		Separador_Jugadas.Add(Etiqueta_Jugadas, 0, 0, 0)

		self.Lista = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_LIST | wx.LC_VRULES)
		Separador_Jugadas.Add(self.Lista, 1, wx.BOTTOM | wx.EXPAND, 5)

		sizer_1 = wx.BoxSizer(wx.VERTICAL)
		Separador_Base.Add(sizer_1, 1, wx.EXPAND, 0)

		self.sizer_PanelTablero = wx.GridSizer(1, 1, 0, 0)
		sizer_1.Add(self.sizer_PanelTablero, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 25)

		self.Panel_Tablero = wx.Panel(self, wx.ID_ANY, style=wx.BORDER_SIMPLE)
		self.Panel_Tablero.SetMinSize((525, 600))
		self.sizer_PanelTablero.Add(self.Panel_Tablero, 0, wx.ALL| wx.EXPAND, 5)
		self.SetSizer(Separador_Base)

		Separador_Info = wx.BoxSizer(wx.HORIZONTAL)
		Separador_Menu.Add(Separador_Info, 0, wx.ALL, 5)

		self.Etiqueta_Info = wx.StaticText(self, wx.ID_ANY, "Se necesita un fichero")
		self.Etiqueta_Info.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "Segoe UI"))
		Separador_Info.Add(self.Etiqueta_Info, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

		self.Layout()

		self.Abrir_Fichero_Image.Bind(wx.EVT_BUTTON, self.OnClick_AbrirFichero)
		self.Nueva_Partida_Image.Bind(wx.EVT_BUTTON, self.OnClick_NuevaPartida)
		self.Grid_Image.Bind(wx.EVT_BUTTON, self.OnClick_NumeroFilas)
		self.Panel_Tablero.Bind(wx.EVT_LEFT_DOWN, self.ClickInicio_MoverBloque)
		self.Panel_Tablero.Bind(wx.EVT_LEFT_UP, self.ClickFin_MoverBloque)
		self.Panel_Tablero.Bind(wx.EVT_SIZE, self.OnValueChanged_Rescalado)

		#Dialogos Principales
		self.dialogAF = Op_AbrirFichero(None, wx.ID_ANY, "")
		self.dialogNP = Op_NuevaPartida(None, wx.ID_ANY, "")
		self.dialogNF = Op_DimensionesTablero(None, wx.ID_ANY, "")
		self.dialogGO = GameOver(None, wx.ID_ANY, "")

		self.datos = [[] for _ in range(filas[0])]
		self.nombre_archivo = ""


	def ClickInicio_MoverBloque(self, event):
		detector_movimiento[0] = wx.GetMousePosition()
		return True

	def ClickFin_MoverBloque(self, event):
		detector_movimiento[1] =  wx.GetMousePosition()
		Movimiento = ""
		Dir = detector_movimiento[1] - detector_movimiento[0]
		#Ancho Columna
		WidthTab = self.Panel_Tablero.GetSize()[0]
		self.ColWidth = WidthTab//(columnas+1)
		self.ColWidth_Extra = WidthTab - (columnas*self.ColWidth)
		#Alto Fila
		HeightTab = self.Panel_Tablero.GetSize()[1]
		self.FilHeight = HeightTab // (filas[0] + 1)
		self.FilHeight_Extra = HeightTab - (filas[0] * self.FilHeight)
		#Detectar donde se ha hecho el click
		ZonaJuegoPos = self.GetPosition() + self.Panel_Tablero.GetPosition()
		ZonaJuegoPos[0] += self.ColWidth_Extra
		RelativePos = detector_movimiento[0] - ZonaJuegoPos
		if RelativePos[0]>0 and RelativePos[1]>0:
			#Dentro de la zona de juego
			ColMov = RelativePos[0] // self.ColWidth
			if ColMov > 9:
				return True
			FilMov = RelativePos[1] // self.FilHeight
			if FilMov > filas[0]:
				return True
			Movimiento += chr(64+FilMov)
			Movimiento += str(ColMov)
			if Dir[1]>10 or Dir[1]<-10:
				#Te mueves en vertical
				return True
			elif Dir[0] > 0:
				Movimiento += '>'
			elif Dir[0] < 0:
				Movimiento += '<'
			else:
				Movimiento = "---"

			#Se comprueba si se puede realizar esa jugada
			MovCorrecto = self.jugada(Movimiento)
			self.Etiqueta_Info.SetForegroundColour(wx.Colour(255, 0, 0))
			if self.nombre_archivo == "":
				self.Etiqueta_Info.SetLabel("Es necesario abrir un fichero")
			elif MovCorrecto == -3:
				self.Etiqueta_Info.SetLabel("Sintaxis incorrecta")
			elif MovCorrecto == -2:
				self.Etiqueta_Info.SetLabel("Movimiento incorrecto")
			elif MovCorrecto == -1:
				self.Etiqueta_Info.SetLabel("No hay ningún bloque ahí")
			else:
				if self.nombre_archivo != "":
					self.Etiqueta_Info.SetLabel("")
					self.Lista.InsertItem(indice[0],Movimiento)
					indice[0] += 1
					time.sleep(0.1)
				
					seguir = True
					while seguir:
						self.caida() 
						lis = self.eliminacion()   
						seguir = len(lis) > 0
						if seguir:
							self.eliminacion()
				
					if(len(self.datos[0]) > 0):
						GameOver.PuntuacionFinal(self.dialogGO, puntos_partida[0])
						self.dialogGO.Centre()
						self.dialogGO.ShowModal()
						self.datos = [[] for _ in range(filas[0])]
						self.Lista.ClearAll()
						indice[0] = 0
						with open(self.nombre_archivo, "r") as fichero:   
							self.iniciar_Juego() 
					else:
						self.Dibujar_Juego_SiguienteFila(wx.ClientDC(self.Panel_Tablero))
						self.Etiqueta_Info.SetForegroundColour(wx.Colour(0, 0, 0))
						self.Etiqueta_Info.SetLabel("Esperando Movimiento")
						
		return True

	def jugada(self, jug):
		# Obtener fila y columna
		fil = ord(jug[0]) - CH_FIL
		col = ord(jug[1]) - CH_COL
		if jug == '---':
			return 0
		if fil < 0 or fil >= filas[0] or col < 0 or col >= columnas:
			return -3
		# Indice del bloque en esa columna
		i = self.index_bloque(self.datos[fil], col)
		if i < 0:
			return -1
		b = self.datos[fil][i]
		# Comprobar si se puede desplazar
		if jug[2] == '<':            
			if i == 0:
				if b.col0 == 0: 
					return -2	
				desp = b.col0
				while desp > 0:
					b.desplazar(-1, 0)
					self.Dibujar_AnimacionMovimiento_Izquierda(wx.ClientDC(self.Panel_Tablero), b)
					desp -= 1
			else:
				ba = self.datos[fil][i - 1]  
				db = b.col0 - ba.col1 - 1   
				if db == 0:
					return -2
				while db > 0:
					b.desplazar(-1, 0)
					self.Dibujar_AnimacionMovimiento_Izquierda(wx.ClientDC(self.Panel_Tablero), b)
					db -= 1
		elif jug[2] == '>':
			if i == len(self.datos[fil])-1:
				if b.col1 == columnas-1: 
					return -2
				desp = columnas-b.col1-1
				while desp > 0:
					b.desplazar(1, 0)
					self.Dibujar_AnimacionMovimiento_Derecha(wx.ClientDC(self.Panel_Tablero), b)
					desp -= 1
			else:
				bs = self.datos[fil][i + 1]  
				db = bs.col0 - b.col1 - 1  
				if db == 0: 
					return -2
				while db > 0:
					b.desplazar(1, 0)
					self.Dibujar_AnimacionMovimiento_Derecha(wx.ClientDC(self.Panel_Tablero), b)
					db -= 1
		else:
			return -3
		return 0

	@staticmethod
	def index_bloque(lis, col):
		i = 0
		for b in lis:
			if b.col0 <= col <= b.col1:
				return i
			i += 1
		return -1

	def OnClick_AbrirFichero(self, event):
		from tkinter import Tk  
		from tkinter.filedialog import askopenfilename
		Tk().withdraw() 
		self.nombre_archivo = askopenfilename()
		try:
			with open(self.nombre_archivo, "r") as fichero:   
				self.datos = [[] for _ in range(filas[0])]
				self.Lista.ClearAll()
				indice[0] = 0
				self.iniciar_Juego() 
		except(Exception):
			self.dialogAF.Centre()
			self.dialogAF.ShowModal()

		return True

	def OnClick_NuevaPartida(self, event):
		self.dialogNP.Centre()
		nueva_partida_id = self.dialogNP.ShowModal()
		try:
			if nueva_partida_id == 5100:
				#Se ha pulsado el botón aceptar
				self.datos = [[] for _ in range(filas[0])]
				self.Lista.ClearAll()
				indice[0] = 0
				self.iniciar_Juego() 
		except(Exception):
			from tkinter import Tk  
			from tkinter.filedialog import askopenfilename
			Tk().withdraw() 
			self.nombre_archivo = askopenfilename()
			try:
				with open(self.nombre_archivo, "r") as fichero:   
					self.tab = Tablero(self.nombre_archivo, filas[0])
					self.iniciar_Juego() 
			except(Exception):
				self.dialogAF.Centre()
				self.dialogAF.ShowModal()


		return True

	def OnClick_NumeroFilas(self, event):
		self.dialogNF.Centre()
		dimensión_tablero_id = self.dialogNF.ShowModal()
		if dimensión_tablero_id == 5100:
			#Se ha pulsado el botón de aceptar
			filas[0] = filas[1]
			self.datos = [[] for _ in range(filas[0])]
			self.Lista.ClearAll()
			indice[0] = 0
			try:
				with open(self.nombre_archivo, "r") as fichero:   
					self.iniciar_Juego() 
			except(Exception):
				from tkinter import Tk  
				from tkinter.filedialog import askopenfilename
				Tk().withdraw() 
				self.nombre_archivo = askopenfilename()
				try:
					with open(self.nombre_archivo, "r") as fichero:   
						self.datos = [[] for _ in range(filas[0])]
						self.Lista.ClearAll()
						indice[0] = 0
						self.iniciar_Juego() 
				except(Exception):
					self.dialogAF.Centre()
					self.dialogAF.ShowModal()
		else:
			Op_DimensionesTablero.UpdateSpinText(self.dialogNF)
		return True

	def OnValueChanged_Rescalado(self, event):
		try:
			self.Dibujar_Juego_Completo(wx.ClientDC(self.Panel_Tablero))
		except(Exception):
			"No se puede imprimir el juego tablero"
			
		return True

	def iniciar_Juego(self):
		#Se pinta el tablero
		self.tab = Tablero(self.nombre_archivo, filas[0])
		puntos_partida[0] = 0
		self.Puntos.SetLabel(str(puntos_partida[0]))
		self.Dibujar_Textos(wx.ClientDC(self.Panel_Tablero))
		self.OnDibujar_Tablero()
		self.Etiqueta_Info.SetForegroundColour(wx.Colour(0, 0, 0))
		self.Etiqueta_Info.SetLabel("Esperando Movimiento")
		return True	
	
	def OnDibujar_Tablero(self):
		try:
			self.Dibujar_Juego_SiguienteFila(wx.ClientDC(self.Panel_Tablero))
		except(Exception):
			"No se puede imprimir"
			
		return True
	
	def Dibujar_Textos(self, dc):
		dc.Clear()
		
		#Datos
		#Alto Fila
		HeightTab = self.Panel_Tablero.GetSize()[1]
		self.FilHeight = HeightTab // (filas[0] + 1)
		self.FilHeight_Extra = HeightTab - (filas[0] * self.FilHeight)
		#Ancho Columna
		WidthTab = self.Panel_Tablero.GetSize()[0]
		self.ColWidth = WidthTab//(columnas+1)
		self.ColWidth_Extra = WidthTab - (columnas*self.ColWidth)

		#Filas
		dc.Pen = wx.Pen(wx.Colour(0,0,0))
		for i in range(filas[0]):
			dc.DrawText(chr(65+i), self.ColWidth_Extra//2, (self.FilHeight//2)+(self.FilHeight*i))
		#Columnas
		for j in range(10):
			dc.DrawText(chr(48+j), self.ColWidth_Extra + self.ColWidth//3 + self.ColWidth*j , self.Panel_Tablero.GetSize()[1] - (self.FilHeight_Extra) + 10 )
		return True

	def Dibujar_Juego_SiguienteFila(self, dc):
		#Datos
		#Alto Fila
		HeightTab = self.Panel_Tablero.GetSize()[1]
		self.FilHeight = HeightTab // (filas[0] + 1)
		#Ancho Columna
		WidthTab = self.Panel_Tablero.GetSize()[0]
		self.ColWidth = WidthTab//(columnas+1)
		self.ColWidth_Extra = WidthTab - (columnas*self.ColWidth)
	
		#Introduce la siguiente línea en datos
		linea = next(entrada[0])
		self.datos[0] = [Bloque(0, c0, c1, val) for (c0, c1, val) in self.bloques_en_linea(linea)]

		#Elementos de dibujo (colores)
		dc.Pen = wx.Pen(wx.Colour(0,0,0))
		self.BlueBrush = wx.Brush(wx.Colour(82, 203, 185)) 
		self.GreenBrush = wx.Brush(wx.Colour(110, 247, 91))
		self.OrangeBrush = wx.Brush(wx.Colour(245, 161, 66))

		for bloque in self.datos[0]:
			if (bloque.val == 0):
				dc.Brush = self.BlueBrush
				dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+(bloque.col0 * self.ColWidth)), 5 + (self.FilHeight*bloque.fila), ((bloque.ancho * self.ColWidth)), (self.FilHeight), 10)
			elif (bloque.val == 1):
				dc.Brush = self.GreenBrush
				dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+(bloque.col0 * self.ColWidth)), 5 + (self.FilHeight*bloque.fila), ((bloque.ancho * self.ColWidth)), (self.FilHeight), 10)
			else:
				dc.Brush = self.OrangeBrush
				dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+(bloque.col0 * self.ColWidth)), 5 + (self.FilHeight*bloque.fila), ((bloque.ancho * self.ColWidth)), (self.FilHeight), 10)
		
		return True

	def Dibujar_Juego_Completo(self, dc):
		#Datos
		#Alto Fila
		HeightTab = self.Panel_Tablero.GetSize()[1]
		self.FilHeight = HeightTab // (filas[0] + 1)
		#Ancho Columna
		WidthTab = self.Panel_Tablero.GetSize()[0]
		self.ColWidth = WidthTab//(columnas+1)
		self.ColWidth_Extra = WidthTab - (columnas*self.ColWidth)

		self.Dibujar_Textos(wx.ClientDC(self.Panel_Tablero))
		
		#Elementos de dibujo (colores)
		dc.Pen = wx.Pen(wx.Colour(0,0,0))
		self.BlueBrush = wx.Brush(wx.Colour(82, 203, 185)) 
		self.GreenBrush = wx.Brush(wx.Colour(110, 247, 91))
		self.OrangeBrush = wx.Brush(wx.Colour(245, 161, 66))
				
		for fila in range(filas[0]):
			for bloque in self.datos[fila]:
				if (bloque.val == 0):
					dc.Brush = self.BlueBrush
					dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+(bloque.col0 * self.ColWidth)), 5 + (self.FilHeight*bloque.fila), ((bloque.ancho * self.ColWidth)), (self.FilHeight), 10)
				elif (bloque.val == 1):
					dc.Brush = self.GreenBrush
					dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+(bloque.col0 * self.ColWidth)), 5 + (self.FilHeight*bloque.fila), ((bloque.ancho * self.ColWidth)), (self.FilHeight), 10)
				else:
					dc.Brush = self.OrangeBrush
					dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+(bloque.col0 * self.ColWidth)), 5 + (self.FilHeight*bloque.fila), ((bloque.ancho * self.ColWidth)), (self.FilHeight), 10)
		
		return True

	def Dibujar_AnimacionCaida(self, dc, bloques_mover):
		#Datos
		#Alto Fila
		HeightTab = self.Panel_Tablero.GetSize()[1]
		self.FilHeight = HeightTab // (filas[0] + 1)
		#Ancho Columna
		WidthTab = self.Panel_Tablero.GetSize()[0]
		self.ColWidth = WidthTab//(columnas+1)
		self.ColWidth_Extra = WidthTab - (columnas*self.ColWidth)

		#Elementos de dibujo (colores)
		self.BlueBrush = wx.Brush(wx.Colour(82, 203, 185)) 
		self.GreenBrush = wx.Brush(wx.Colour(110, 247, 91))
		self.OrangeBrush = wx.Brush(wx.Colour(245, 161, 66))
		self.Goma = wx.Brush(wx.Colour(240, 240, 240))
		self.GomaFina = wx.Pen(wx.Colour(240, 240, 240))
				
		time.sleep(0.05)
		#Borrar
		dc.Brush = self.Goma
		dc.Pen = self.GomaFina
		for bloq in bloques_mover:
			dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+((bloq.col0) * self.ColWidth)), 5 + (self.FilHeight*(bloq.fila-1)), ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)

		#Pintas
		dc.Pen = wx.Pen(wx.Colour(0,0,0))
		for bloq in bloques_mover:
			if (bloq.val == 0):
				dc.Brush = self.BlueBrush
				dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+(bloq.col0 * self.ColWidth)), 5 + (self.FilHeight*bloq.fila) - self.FilHeight//2 , ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
			elif (bloq.val == 1):
				dc.Brush = self.GreenBrush
				dc.DrawRoundedRectangle ((self.ColWidth_Extra-5+(bloq.col0 * self.ColWidth)), 5 + (self.FilHeight*bloq.fila) - self.FilHeight//2, ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
			else:
				dc.Brush = self.OrangeBrush
				dc.DrawRoundedRectangle ((self.ColWidth_Extra-5+(bloq.col0 * self.ColWidth)), 5 + (self.FilHeight*bloq.fila) - self.FilHeight//2, ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)

		time.sleep(0.05)
		#Borrar
		dc.Brush = self.Goma
		dc.Pen = self.GomaFina
		for bloq in bloques_mover:
			dc.DrawRoundedRectangle ((self.ColWidth_Extra-5+(bloq.col0 * self.ColWidth)), 5 + (self.FilHeight*bloq.fila) - self.FilHeight//2, ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)

		#Pintar
		dc.Pen = wx.Pen(wx.Colour(0,0,0))
		for bloq in bloques_mover:
			if (bloq.val == 0):
				dc.Brush = self.BlueBrush
				dc.DrawRoundedRectangle( (self.ColWidth_Extra-5+(bloq.col0 * self.ColWidth)), 5 + (self.FilHeight*bloq.fila), ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
			elif (bloq.val == 1):
				dc.Brush = self.GreenBrush
				dc.DrawRoundedRectangle( (self.ColWidth_Extra-5+(bloq.col0 * self.ColWidth)), 5 + (self.FilHeight*bloq.fila), ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
			else:
				dc.Brush = self.OrangeBrush
				dc.DrawRoundedRectangle( (self.ColWidth_Extra-5+(bloq.col0 * self.ColWidth)), 5 + (self.FilHeight*bloq.fila), ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
		
		return True
	
	def Dibujar_AnimacionMovimiento_Derecha(self, dc, bloq):
		#Datos
		#Alto Fila
		HeightTab = self.Panel_Tablero.GetSize()[1]
		self.FilHeight = HeightTab // (filas[0] + 1)
		#Ancho Columna
		WidthTab = self.Panel_Tablero.GetSize()[0]
		self.ColWidth = WidthTab//(columnas+1)
		self.ColWidth_Extra = WidthTab - (columnas*self.ColWidth)
		
		#Elementos de dibujo (colores)
		self.BlueBrush = wx.Brush(wx.Colour(82, 203, 185)) 
		self.GreenBrush = wx.Brush(wx.Colour(110, 247, 91))
		self.OrangeBrush = wx.Brush(wx.Colour(245, 161, 66))
		self.Goma = wx.Brush(wx.Colour(240, 240, 240))
		self.GomaFina = wx.Pen(wx.Colour(240, 240, 240))

		time.sleep(0.05)

		dc.Brush = self.Goma
		dc.Pen = self.GomaFina
		dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+((bloq.col0-1) * self.ColWidth)), 5 + (self.FilHeight*bloq.fila), ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
		dc.Pen = wx.Pen(wx.Colour(0,0,0))

		if (bloq.val == 0):
			dc.Brush = self.BlueBrush
			dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+(bloq.col0 * self.ColWidth) - self.ColWidth//2), 5 + (self.FilHeight*bloq.fila), ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
		elif (bloq.val == 1):
			dc.Brush = self.GreenBrush
			dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+(bloq.col0 * self.ColWidth) - self.ColWidth//2), 5 + (self.FilHeight*bloq.fila), ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
		else:
			dc.Brush = self.OrangeBrush
			dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+(bloq.col0 * self.ColWidth) - self.ColWidth//2), 5 + (self.FilHeight*bloq.fila), ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
		
		time.sleep(0.05)
		dc.Brush = self.Goma
		dc.Pen = self.GomaFina
		dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+(bloq.col0 * self.ColWidth) - self.ColWidth//2), 5 + (self.FilHeight*bloq.fila), ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
		dc.Pen = wx.Pen(wx.Colour(0,0,0))

		if (bloq.val == 0):
			dc.Brush = self.BlueBrush
			dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+(bloq.col0 * self.ColWidth)), 5 + (self.FilHeight*bloq.fila), ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
		elif (bloq.val == 1):
			dc.Brush = self.GreenBrush
			dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+(bloq.col0 * self.ColWidth)), 5 + (self.FilHeight*bloq.fila), ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
		else:
			dc.Brush = self.OrangeBrush
			dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+(bloq.col0 * self.ColWidth)), 5 + (self.FilHeight*bloq.fila), ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
		return True

	def Dibujar_AnimacionMovimiento_Izquierda(self, dc, bloq):
		#Datos
		#Alto Fila
		HeightTab = self.Panel_Tablero.GetSize()[1]
		self.FilHeight = HeightTab // (filas[0] + 1)
		#Ancho Columna
		WidthTab = self.Panel_Tablero.GetSize()[0]
		self.ColWidth = WidthTab//(columnas+1)
		self.ColWidth_Extra = WidthTab - (columnas*self.ColWidth)
		
		#Elementos de dibujo (colores)
		self.BlueBrush = wx.Brush(wx.Colour(82, 203, 185)) 
		self.GreenBrush = wx.Brush(wx.Colour(110, 247, 91))
		self.OrangeBrush = wx.Brush(wx.Colour(245, 161, 66))
		self.Goma = wx.Brush(wx.Colour(240, 240, 240))
		self.GomaFina = wx.Pen(wx.Colour(240, 240, 240))

		time.sleep(0.05)

		dc.Brush = self.Goma
		dc.Pen = self.GomaFina
		dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+((bloq.col0+1) * self.ColWidth)), 5 + (self.FilHeight*bloq.fila), ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
		dc.Pen = wx.Pen(wx.Colour(0,0,0))

		if (bloq.val == 0):
			dc.Brush = self.BlueBrush
			dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+(bloq.col0 * self.ColWidth) + self.ColWidth//2), 5 + (self.FilHeight*bloq.fila), ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
		elif (bloq.val == 1):
			dc.Brush = self.GreenBrush
			dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+(bloq.col0 * self.ColWidth) + self.ColWidth//2), 5 + (self.FilHeight*bloq.fila), ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
		else:
			dc.Brush = self.OrangeBrush
			dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+(bloq.col0 * self.ColWidth) + self.ColWidth//2), 5 + (self.FilHeight*bloq.fila), ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
		
		time.sleep(0.05)
		dc.Brush = self.Goma
		dc.Pen = self.GomaFina
		dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+(bloq.col0 * self.ColWidth) + self.ColWidth//2), 5 + (self.FilHeight*bloq.fila), ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
		dc.Pen = wx.Pen(wx.Colour(0,0,0))

		if (bloq.val == 0):
			dc.Brush = self.BlueBrush
			dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+(bloq.col0 * self.ColWidth)), 5 + (self.FilHeight*bloq.fila), ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
		elif (bloq.val == 1):
			dc.Brush = self.GreenBrush
			dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+(bloq.col0 * self.ColWidth)), 5 + (self.FilHeight*bloq.fila), ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
		else:
			dc.Brush = self.OrangeBrush
			dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+(bloq.col0 * self.ColWidth)), 5 + (self.FilHeight*bloq.fila), ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
		return True
	
	def Dibujar_AnimaciónDestruir_Fila(self, dc, fila):
		#Datos
		#Alto Fila
		HeightTab = self.Panel_Tablero.GetSize()[1]
		self.FilHeight = HeightTab // (filas[0] + 1)
		#Ancho Columna
		WidthTab = self.Panel_Tablero.GetSize()[0]
		self.ColWidth = WidthTab//(columnas+1)
		self.ColWidth_Extra = WidthTab - (columnas*self.ColWidth)
		
		#Elementos de dibujo (colores)
		self.BlueBrush = wx.Brush(wx.Colour(82, 203, 185)) 
		self.GreenBrush = wx.Brush(wx.Colour(110, 247, 91))
		self.OrangeBrush = wx.Brush(wx.Colour(245, 161, 66))
		self.Goma = wx.Brush(wx.Colour(240, 240, 240))
		self.GomaFina = wx.Pen(wx.Colour(240, 240, 240))

		#Borrar
		time.sleep(0.1)
		dc.Brush = self.Goma
		dc.Pen = self.GomaFina
		for bloq in self.datos[fila]:
			dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+((bloq.col0) * self.ColWidth)), 5 + (self.FilHeight*bloq.fila), ((bloq.ancho * self.ColWidth)), (self.FilHeight), 10)
		

		#Pintar
		dc.Pen = wx.Pen(wx.Colour(0,0,0))
		for bloq in self.datos[fila]:
			if (bloq.val == 0):
				dc.Brush = self.BlueBrush
				dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+((bloq.col0) * self.ColWidth)), 5 + (self.FilHeight*bloq.fila) + self.FilHeight//2, ((bloq.ancho * self.ColWidth)), (self.FilHeight//2), 10)
			elif (bloq.val == 1):
				dc.Brush = self.GreenBrush
				dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+((bloq.col0) * self.ColWidth)), 5 + (self.FilHeight*bloq.fila) + self.FilHeight//2, ((bloq.ancho * self.ColWidth)), (self.FilHeight//2), 10)
			else:
				dc.Brush = self.OrangeBrush
				dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+((bloq.col0) * self.ColWidth)), 5 + (self.FilHeight*bloq.fila) + self.FilHeight//2, ((bloq.ancho * self.ColWidth)), (self.FilHeight//2), 10)
		
		#Borrar
		time.sleep(0.1)
		dc.Brush = self.Goma
		dc.Pen = self.GomaFina
		for bloq in self.datos[fila]:
			dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+((bloq.col0) * self.ColWidth)), 5 + (self.FilHeight*bloq.fila) + self.FilHeight//2, ((bloq.ancho * self.ColWidth)), (self.FilHeight//2), 10)
		
		#Pintar
		dc.Pen = wx.Pen(wx.Colour(0,0,0))
		for bloq in self.datos[fila]:
			if (bloq.val == 0):
				dc.Brush = self.BlueBrush
				dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+((bloq.col0) * self.ColWidth)), 5 + (self.FilHeight*bloq.fila) + (3*self.FilHeight)//4, ((bloq.ancho * self.ColWidth)), (self.FilHeight//4), 10)
			elif (bloq.val == 1):
				dc.Brush = self.GreenBrush
				dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+((bloq.col0) * self.ColWidth)), 5 + (self.FilHeight*bloq.fila) + (3*self.FilHeight)//4, ((bloq.ancho * self.ColWidth)), (self.FilHeight//4), 10)
			else:
				dc.Brush = self.OrangeBrush
				dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+((bloq.col0) * self.ColWidth)), 5 + (self.FilHeight*bloq.fila) + (3*self.FilHeight)//4, ((bloq.ancho * self.ColWidth)), (self.FilHeight//4), 10)

		#Borrar
		time.sleep(0.1)
		dc.Brush = self.Goma
		dc.Pen = self.GomaFina
		for bloq in self.datos[fila]:
			dc.DrawRoundedRectangle ( (self.ColWidth_Extra-5+((bloq.col0) * self.ColWidth)), 5 + (self.FilHeight*bloq.fila) + (3*self.FilHeight)//4, ((bloq.ancho * self.ColWidth)), (self.FilHeight//4), 10)

		return True

	@staticmethod
	def bloques_en_linea(lin):
		inicio, ancho, caracter_anterior = 0, 0, ' '
		for caracter in lin:
			if caracter != caracter_anterior:
				if caracter_anterior != ' ':
					yield (inicio-ancho, inicio-1, ord(caracter_anterior.upper())-CH_FICH)	#Columna inicial - Columna Final - Color
				caracter_anterior = caracter
				ancho = 1
			else:
				ancho += 1
			inicio += 1
		if caracter_anterior != ' ':
			yield (inicio-ancho, inicio-1, ord(caracter_anterior.upper())-CH_FICH)
	
	def caida(self):
		for i in range(filas[0]):
			Cambio = False
			lista_bloques_caidos =[]
			for fil_ori in range(filas[0]-2, -1, -1):
            	# Se recorren los bloques de la fila
				for b in self.datos[fil_ori][:]:
					# Se comprueban huecos en filas inferiores
					fil_des = pos_hueco = -1
					for i in range(fil_ori+1, fil_ori+2):
						ph = self.pos_ins_bloque(self.datos[i], b)
						if ph == -1:
							break
						pos_hueco = ph
						fil_des = i
                	# Si hay descenso, mover el bloque
					if fil_des > -1:
						Cambio = True
						self.datos[fil_ori].remove(b)
						self.datos[fil_des].insert(pos_hueco, b)
						b.desplazar(0, fil_des - fil_ori)
						lista_bloques_caidos.append(b)
			if Cambio:
				self.Dibujar_AnimacionCaida(wx.ClientDC(self.Panel_Tablero), lista_bloques_caidos)
			
		return True

	@staticmethod    
	def pos_ins_bloque(lis, blo):
		# Búsqueda del primer bloque totalmente posterior al nuestro
		i = 0
		for b in lis:
			if b.col0 > blo.col1:
				break
			i += 1
		# Si existe colisión, es con el bloque anterior al posterior
		return i if i == 0 or lis[i-1].col1 < blo.col0 else -1

	def eliminacion(self):
		lis = []
		reaccion_cadena = False
		inc_ptos = 0
		for fil in range(filas[0]):
			if self.fila_completa(self.datos[fil], columnas):
				if self.fila_mismo_color(self.datos[fil]):
					reaccion_cadena = True
					break
				self.Dibujar_AnimaciónDestruir_Fila(wx.ClientDC(self.Panel_Tablero), fil)
				lis += self.borra_fila(fil)
				inc_ptos += columnas
		if reaccion_cadena:
			for fil in range(filas[0]):
				inc_ptos += sum((b.ancho for b in self.datos[fil]))
				self.Dibujar_AnimaciónDestruir_Fila(wx.ClientDC(self.Panel_Tablero), fil)
				lis += self.borra_fila(fil)
		puntos_partida[0] += inc_ptos
		self.Puntos.SetLabel(str(puntos_partida[0]))
		return lis
	
	def borra_fila(self, fil):
		lis = self.datos[fil]
		self.datos[fil] = []
		return lis

	@staticmethod
	def fila_completa(fila, numcol):
		if len(fila) == 0:
			return False
		# Comprobación de que los bloques inicial y final cubren los extremos 
		if fila[0].col0 != 0 or fila[-1].col1 != numcol-1:
			return False
		for (b1, b2) in zip(fila, fila[1:]):
			if b1.col1+1 != b2.col0:
				return False
		return True

	@staticmethod
	def fila_mismo_color(fila):
		return all(map(lambda b: b.val == fila[0].val, fila[1:]))
		
#Dialogo Error al abrir fichero
class Op_AbrirFichero(wx.Dialog):
	def __init__(self, parent = None, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.CAPTION
		wx.Dialog.__init__(self, parent, *args, **kwds)
		self.SetSize((300, 125))
		self.SetTitle("")

		Sizer_BaseAF = wx.BoxSizer(wx.VERTICAL)

		Etiqueta_Error = wx.StaticText(self, wx.ID_ANY, "Se ha producido un error")
		Etiqueta_Error.SetMinSize((245, 27))
		Etiqueta_Error.SetFont(wx.Font(17, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, 0, ""))
		Sizer_BaseAF.Add(Etiqueta_Error, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)

		Sizer_ButtonAF = wx.StdDialogButtonSizer()
		Sizer_BaseAF.Add(Sizer_ButtonAF, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 4)

		self.ButtonAF = wx.Button(self, wx.ID_OK, "")
		self.ButtonAF.SetDefault()
		Sizer_ButtonAF.AddButton(self.ButtonAF)

		Sizer_ButtonAF.Realize()

		self.SetSizer(Sizer_BaseAF)

		self.SetAffirmativeId(self.ButtonAF.GetId())

		self.Layout()

#Dialogo Nueva Partida
class Op_NuevaPartida(wx.Dialog):
	def __init__(self, parent = None, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.CAPTION | wx.SYSTEM_MENU
		wx.Dialog.__init__(self, parent, *args, **kwds)
		self.SetSize((300, 150))
		self.SetTitle("Opciones de Deslizator")

		Separador_Dialog_AbrirFichero = wx.BoxSizer(wx.VERTICAL)

		Etiqueta_NuevaPartida = wx.StaticText(self, wx.ID_ANY, "Nueva Partida:")
		Etiqueta_NuevaPartida.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
		Separador_Dialog_AbrirFichero.Add(Etiqueta_NuevaPartida, 0, wx.ALL, 5)

		Separador_Seguro = wx.BoxSizer(wx.VERTICAL)
		Separador_Dialog_AbrirFichero.Add(Separador_Seguro, 1, wx.ALIGN_CENTER_HORIZONTAL, 0)

		Etiqueta_Seguro = wx.StaticText(self, wx.ID_ANY, u"¿Seguro que quieres empezar una nueva partida?")
		Separador_Seguro.Add(Etiqueta_Seguro, 0, wx.ALL, 5)

		Sizer_Botones_NP = wx.StdDialogButtonSizer()
		Separador_Dialog_AbrirFichero.Add(Sizer_Botones_NP, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		self.Op_NP_Aceptar = wx.Button(self, wx.ID_OK, "Aceptar")
		self.Op_NP_Aceptar.SetDefault()
		Sizer_Botones_NP.AddButton(self.Op_NP_Aceptar)

		self.Op_NP_Cancelar = wx.Button(self, wx.ID_CANCEL, "Cancelar")
		Sizer_Botones_NP.AddButton(self.Op_NP_Cancelar)

		Sizer_Botones_NP.Realize()

		self.SetSizer(Separador_Dialog_AbrirFichero)

		self.SetAffirmativeId(self.Op_NP_Aceptar.GetId())
		self.SetEscapeId(self.Op_NP_Cancelar.GetId())

		self.Layout()
		self.Centre()	

#Dialogo Dimensiones Tablero
class Op_DimensionesTablero(wx.Dialog):
	def __init__(self, parent = None, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.CAPTION | wx.SYSTEM_MENU
		wx.Dialog.__init__(self, parent, *args, **kwds)
		self.SetSize((300, 150))
		self.SetTitle("Opciones de Deslizator")

		Separador_Dialog_Tablero = wx.BoxSizer(wx.VERTICAL)

		Etiqueta_DimensionesTablero = wx.StaticText(self, wx.ID_ANY, "Dimensiones tablero:")
		Etiqueta_DimensionesTablero.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
		Separador_Dialog_Tablero.Add(Etiqueta_DimensionesTablero, 0, wx.ALL, 5)

		Separador_NFilas = wx.BoxSizer(wx.HORIZONTAL)
		Separador_Dialog_Tablero.Add(Separador_NFilas, 1, 0, 0)

		Etiqueta_NFilas = wx.StaticText(self, wx.ID_ANY, u"NºFilas :")
		Separador_NFilas.Add(Etiqueta_NFilas, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		self.Spin_NFilas = wx.SpinCtrl(self, wx.ID_ANY, min=10, max=20)
		self.Spin_NFilas.SetValue(filas[0])
		self.Spin_NFilas.SetMinSize((60, 23))
		self.Spin_NFilas.Bind(wx.EVT_TEXT, self.OnValueChanged_NFilas, self.Spin_NFilas)
		
		Separador_NFilas.Add(self.Spin_NFilas, 0, wx.ALIGN_CENTER_VERTICAL, 0)

		sizer_2 = wx.StdDialogButtonSizer()
		Separador_Dialog_Tablero.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		self.Op_DT_Aceptar = wx.Button(self, wx.ID_OK, "Aceptar")
		self.Op_DT_Aceptar.SetDefault()
		sizer_2.AddButton(self.Op_DT_Aceptar)

		self.Op_DT_Cancelar = wx.Button(self, wx.ID_CANCEL, "Cancelar")
		sizer_2.AddButton(self.Op_DT_Cancelar)

		sizer_2.Realize()

		self.SetSizer(Separador_Dialog_Tablero)

		self.SetAffirmativeId(self.Op_DT_Aceptar.GetId())
		self.SetEscapeId(self.Op_DT_Cancelar.GetId())
		
		self.Layout()
		self.Centre()

	def UpdateSpinText (self):
		self.Spin_NFilas.SetValue(filas[0])
	
	def OnValueChanged_NFilas(self, event):
		filas[1] = self.Spin_NFilas.GetValue()

#Dialogo Game Over
class GameOver(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0)
		wx.Dialog.__init__(self, *args, **kwds)
		self.SetSize((400, 150))
		self.SetTitle("GameOver")

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		GAMEOVER_Text = wx.StaticText(self, wx.ID_ANY, "GAME OVER")
		GAMEOVER_Text.SetFont(wx.Font(30, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 1, ""))
		sizer_1.Add(GAMEOVER_Text, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)

		sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)

		label_1 = wx.StaticText(self, wx.ID_ANY, u"Puntuación Total:")
		label_1.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
		sizer_3.Add(label_1, 0, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM | wx.LEFT | wx.TOP, 15)

		self.PuntuacionFinal = wx.StaticText(self, wx.ID_ANY, str(puntos_partida[0]))
		sizer_3.Add(self.PuntuacionFinal, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 4)

		self.button_CLOSE = wx.Button(self, wx.ID_CLOSE, "")
		sizer_2.AddButton(self.button_CLOSE)

		sizer_2.Realize()

		self.SetSizer(sizer_1)

		self.SetEscapeId(self.button_CLOSE.GetId())

		self.Layout()

	def PuntuacionFinal(self, cad):
		self.PuntuacionFinal.SetLabel(str(cad))
		return True

if __name__ == "__main__":
	Deslizator_JavierRamosJimeno = Deslizator(0)
	Deslizator_JavierRamosJimeno.MainLoop()

