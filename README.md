# 🚢 Puerto de Chancay - Sistema de Gestión Inteligente

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect%20with%20Victor-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/victorcabrejos/)

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/FastAPI-Latest-00a393.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991.svg" alt="OpenAI">
  <img src="https://img.shields.io/badge/Architecture-Hexagonal-ff6b6b.svg" alt="Hexagonal Architecture">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</div>

<div align="center">
  <h3>🤖 Sistema portuario inteligente con Arquitectura Hexagonal + IA</h3>
  <p><em>Demostrando Clean Architecture, Domain-Driven Design y integración con OpenAI GPT-4o mini</em></p>
</div>

---

## 🌟 **¿Qué es este proyecto?**

Un **sistema de gestión portuaria inteligente** del Puerto de Chancay que demuestra:

- ✅ **Arquitectura Hexagonal** (Ports & Adapters) - Intercambiabilidad y testabilidad
- ✅ **Integración con IA** (OpenAI GPT-4o mini) - Predicciones y análisis inteligente
- ✅ **Frontend Moderno** (Tailwind CSS + Glassmorphism) - UI/UX profesional
- ✅ **API REST** (FastAPI) - Documentación automática y alto rendimiento
- ✅ **Domain-Driven Design** - Modelado del negocio portuario

## � **¿Por qué Puerto de Chancay?**

**Chancay** será el puerto más moderno de Latinoamérica, conectando directamente **Perú con Asia**. Este proyecto simula cómo la tecnología puede revolucionar la gestión portuaria del futuro.

## �️ **Arquitectura del Sistema**

### Arquitectura Hexagonal (Clean Architecture)

```
📁 domain/          # 💎 Núcleo del negocio (sin dependencias externas)
├── entities.py     # Entidades: Container, Ship, PortOperation, AIInsight
├── ports.py        # Interfaces: DataRepository, AIService
└── services.py     # Lógica de negocio pura

� adapters/        # 🔌 Implementaciones intercambiables
├── data_adapter.py     # CSV → PostgreSQL/MongoDB (intercambiable)
└── openai_adapter.py   # OpenAI → Claude/Gemini (intercambiable)

📁 api/             # 🌐 Interfaz web
└── controller.py   # Endpoints REST (FastAPI)

📁 templates/       # 🎨 Frontend moderno
├── landing.html    # Página de presentación
└── index.html      # Dashboard operativo
```

### 🔄 **Beneficios de la Arquitectura**

| Principio | Beneficio | Ejemplo |
|-----------|-----------|---------|
| **Intercambiabilidad** | Cambiar implementaciones sin tocar lógica | CSV → PostgreSQL sin modificar servicios |
| **Testabilidad** | Mock fácil de dependencias | Test unitarios con datos simulados |
| **Mantenibilidad** | Separación clara de responsabilidades | Cambios UI no afectan lógica de negocio |
| **Escalabilidad** | Agregar funcionalidades independientemente | Nuevos adapters sin tocar el core |

## 🤖 **Capacidades de Inteligencia Artificial**

### Predicciones y Análisis:
- 🔮 **Predicción de Congestión** - Análisis predictivo del tráfico portuario
- 🛣️ **Optimización de Rutas** - Sugerencias para mejores rutas de descarga
- 🚨 **Detección de Anomalías** - Identificación automática de problemas
- 📈 **Análisis de Patrones** - Insights sobre flujos de carga y eficiencia

### Ejemplo de Insight Generado:
```json
{
  "title": "Optimización de Grúas en Muelle 3",
  "description": "Se detecta subutilización del 23% en grúas del muelle 3 entre 14:00-16:00",
  "confidence": 0.87,
  "impact_level": "medium",
  "type": "efficiency"
}
```

## 🚀 **Instalación y Ejecución**

### Prerrequisitos
- Python 3.11+
- Conda/Miniconda
- OpenAI API Key

### 1. Clonar el repositorio
```bash
git clone https://github.com/VictorCabrejos/puerto-chancay-hexagonal-ai.git
cd puerto-chancay-hexagonal-ai
```

### 2. Crear entorno virtual
```bash
conda create -n chancay_env python=3.11
conda activate chancay_env
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar OpenAI API Key
```bash
# IMPORTANTE: Obtén tu API key en https://platform.openai.com/api-keys

# Opción 1: Variable de entorno (RECOMENDADO)
export OPENAI_API_KEY="sk-proj-tu-api-key-aqui"

# Opción 2: Windows
set OPENAI_API_KEY=sk-proj-tu-api-key-aqui

# Opción 3: Crear archivo .env
echo "OPENAI_API_KEY=sk-proj-tu-api-key-aqui" > .env
```

### 5. Ejecutar el sistema
```bash
uvicorn app:app --host 0.0.0.0 --port 5000 --reload
```

### 6. Acceder al sistema
- 🏠 **Landing Page**: http://localhost:5000/landing
- 📊 **Dashboard**: http://localhost:5000
- � **API Docs**: http://localhost:5000/docs

## 📊 **Funcionalidades del Dashboard**

### 📈 Vista General del Puerto
- **Estadísticas en tiempo real** (contenedores, barcos, eficiencia)
- **Estado de embarcaciones** (llegando, atracado, descargando, completado)
- **Métricas de rendimiento** con comparación mundial
- **Capacidad e infraestructura** del puerto

### 🔍 Monitoreo Detallado
- **Tracking de contenedores** individual con progreso visual
- **Gestión de grúas** y asignación optimizada
- **Status aduanero** y documentación
- **Alertas automáticas** basadas en IA

### 🌏 Conectividad Perú-Asia
- **Rutas comerciales activas** en tiempo real
- **Análisis de origen/destino** de mercancías
- **Comparación de tiempos** vs rutas tradicionales
- **Impacto económico** del nuevo corredor

## 🌐 **API REST Endpoints**

| Endpoint | Método | Descripción | Ejemplo Response |
|----------|--------|-------------|------------------|
| `/` | GET | Dashboard principal | HTML Page |
| `/landing` | GET | Página de presentación | HTML Page |
| `/api/overview` | GET | Resumen del puerto | `{"total_containers": 1547, "efficiency": 0.89}` |
| `/api/ships` | GET | Estado de barcos | `[{"ship_name": "COSCO Beijing", "status": "atracado"}]` |
| `/api/containers` | GET | Lista de contenedores | `[{"container_id": "TEMU7834561", "status": "descargando"}]` |
| `/api/efficiency` | GET | Métricas de eficiencia | `{"containers_per_hour": 45.2, "rotation_time": 8.3}` |
| `/api/ai-insights` | GET | Insights de IA | `[{"title": "Congestión detectada", "confidence": 0.92}]` |

## 🎨 **Stack Tecnológico**

### Backend
- **FastAPI** - Framework web moderno y rápido
- **Python 3.11** - Lenguaje de programación
- **OpenAI GPT-4o mini** - Inteligencia artificial
- **Pandas** - Procesamiento de datos
- **Uvicorn** - Servidor ASGI de alto rendimiento

### Frontend
- **Tailwind CSS** - Framework CSS utility-first
- **JavaScript ES6+** - Programación moderna
- **SVG Icons** - Iconografía profesional y escalable
- **Glassmorphism** - Efectos visuales modernos

### Arquitectura
- **Hexagonal Architecture** - Ports & Adapters pattern
- **Domain-Driven Design** - Modelado orientado al dominio
- **Dependency Injection** - Inversión de dependencias
- **SOLID Principles** - Principios de diseño

## � **Impacto del Puerto de Chancay**

### 📊 Datos Clave
- **Capacidad**: 1.5 millones TEU anuales (fase 1)
- **Profundidad**: 17.8 metros (permite megabuques)
- **Ubicación**: 78 km al norte de Lima, Perú
- **Inversión**: USD 3,500 millones
- **Ahorro logístico**: 7-10 días vs rutas tradicionales

### 💰 Beneficios Económicos
- **Reducción de costos** logísticos en 20%
- **Incremento del comercio** Perú-Asia en 30%
- **Generación de empleos**: 8,000 directos + 40,000 indirectos
- **Posicionamiento**: Perú como hub del Pacífico Sur

## � **Roadmap y Futuras Expansiones**

### Técnicas
- [ ] **Microservicios** - Dividir en servicios especializados
- [ ] **Containerización** - Docker + Kubernetes
- [ ] **Base de datos** - PostgreSQL/MongoDB para producción
- [ ] **Machine Learning** - Modelos personalizados de predicción
- [ ] **Real-time** - WebSockets para actualizaciones en vivo

### Funcionales
- [ ] **Gestión de inventario** automatizada
- [ ] **Integración aduanera** en tiempo real
- [ ] **IoT Tracking** - Sensores en contenedores
- [ ] **Analytics avanzados** - Dashboards ejecutivos
- [ ] **Mobile App** - Aplicación para dispositivos móviles

## 🤝 **Contribuciones**

¿Quieres contribuir al proyecto? ¡Excelente!

1. **Fork** el repositorio
2. **Crea** una branch para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. **Push** a la branch (`git push origin feature/nueva-funcionalidad`)
5. **Abre** un Pull Request

### Áreas donde puedes contribuir:
- 🐛 **Bug fixes** y mejoras de rendimiento
- 🎨 **UI/UX** improvements
- 🧠 **Nuevos algoritmos** de IA
- 📚 **Documentación** y ejemplos
- 🧪 **Tests** unitarios e integración

## 📄 **Licencia**

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 🙏 **Agradecimientos**

- **OpenAI** por la API GPT-4o mini
- **FastAPI** por el excelente framework
- **Tailwind CSS** por el sistema de diseño
- **Puerto de Chancay** por la inspiración del proyecto

---

<div align="center">
  <h3>🚢 Construyendo el futuro del comercio internacional con arquitectura inteligente</h3>
  <p>Hecho con ❤️ para demostrar Clean Architecture + IA</p>

  **[🌐 Demo en Vivo](http://localhost:5000)** | **[📖 Documentación](http://localhost:5000/docs)** | **[🎯 Casos de Uso](./docs/use-cases.md)**
</div>
- **Tiempo de Rotación:** 36-48 horas
- **Utilización de Grúas:** 70-95%
- **Ocupación de Muelles:** 60-90%

### 🔮 Futuras Extensiones

1. **IoT Integration**
   - Sensores en contenedores
   - Tracking GPS en tiempo real
   - Monitoreo ambiental

2. **Blockchain**
   - Trazabilidad inmutable
   - Smart contracts para operaciones
   - Transparencia en la cadena de suministro

3. **Machine Learning Avanzado**
   - Modelos predictivos personalizados
   - Optimización automática de recursos
   - Detección de anomalías

4. **Integración Regional**
   - Conexión con otros puertos
   - Red logística América Latina
   - Optimización de rutas continentales

### 👥 Equipo de Desarrollo

Sistema desarrollado para demostrar los beneficios de la **Arquitectura Hexagonal** en aplicaciones de misión crítica como la gestión portuaria del Puerto de Chancay.

---

**🇵🇪 Impulsando el comercio Perú-Asia con tecnología de vanguardia 🌏**
