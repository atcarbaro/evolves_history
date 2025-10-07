"""
REST API using FastAPI for Digimon evolution line service

To use this API:
1. Install FastAPI and Uvicorn: pip install fastapi uvicorn
2. Run: uvicorn api:app --reload
3. Access: http://localhost:8000/docs for interactive documentation
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from digimon_service import DigimonEvolutionService
import json

# Initialize FastAPI
app = FastAPI(
    title="Digimon Evolution API",
    description="REST API to query Digimon evolution lines",
    version="1.0.0"
)

# Configure CORS to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize service (global for reuse)
service = None


# Pydantic models for response
class DigimonBase(BaseModel):
    name: str
    stage: str
    number: Optional[int]


class CurrentDigimon(BaseModel):
    name: str
    number: Optional[int]
    stage: str
    attribute: str


class EvolutionLineResponse(BaseModel):
    currentDigimon: CurrentDigimon
    preEvolutions: List[DigimonBase]
    postEvolutions: List[DigimonBase]


class ErrorResponse(BaseModel):
    error: bool
    message: str


@app.on_event("startup")
async def startup_event():
    """Initialize service on application startup"""
    global service
    try:
        # Try production path first, fallback to development path
        import os
        
        # For Vercel deployment
        base_dir = os.path.dirname(os.path.abspath(__file__))
        excel_path = os.path.join(base_dir, '..', 'data', 'digimon_list.xlsx')
        
        # Fallback for local development
        if not os.path.exists(excel_path):
            excel_path = 'data/digimon_list.xlsx'
        
        service = DigimonEvolutionService(excel_path)
        print("✅ Digimon service initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing service: {e}")
        import traceback
        traceback.print_exc()


# For local development
if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.environ.get("PORT", 8000))
    
    print("\n🚀 Starting Digimon Evolution API...")
    print(f"📚 Documentation available at: http://localhost:{port}/docs")
    print(f"🔗 API available at: http://localhost:{port}\n")
    
    uvicorn.run(app, host="0.0.0.0", port=port)

@app.get("/", tags=["General"])
async def root():
    """Root welcome endpoint"""
    return {
        "message": "🌟 Digimon Evolution API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "search_evolution": "/api/evolution/{digimon_name}",
            "next_evolutions": "/api/evolution/{digimon_name}/next",
            "previous_evolutions": "/api/evolution/{digimon_name}/previous",
            "can_evolve": "/api/can-evolve/{from_digimon}/{to_digimon}",
            "health": "/health"
        }
    }


@app.get("/health", tags=["General"])
async def health_check():
    """Check API health status"""
    if service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    return {
        "status": "healthy",
        "service": "online"
    }


@app.get("/api/evolution/{digimon_name}", response_model=EvolutionLineResponse, tags=["Evolution"])
async def get_evolution(digimon_name: str):
    """
    Get complete evolution line for a Digimon
    
    Args:
        digimon_name: Name of the Digimon to search
        
    Returns:
        Complete evolution line (pre-evolutions and post-evolutions)
        
    Example response:
    ```json
    {
      "currentDigimon": {
        "name": "Patamon",
        "number": 51,
        "stage": "III",
        "attribute": "Data"
      },
      "preEvolutions": [
        {
          "name": "Tokomon",
          "stage": "II",
          "number": 13
        }
      ],
      "postEvolutions": [
        {
          "name": "Angemon",
          "stage": "IV",
          "number": 84
        }
      ]
    }
    ```
    """
    if service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        result_json = service.get_evolution_line(digimon_name)
        result = json.loads(result_json)
        
        # Check if there's an error
        if 'error' in result and result['error']:
            raise HTTPException(status_code=404, detail=result['message'])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.get("/api/evolution/{digimon_name}/next", tags=["Evolution"])
async def get_next_evolutions(digimon_name: str):
    """
    Get only post-evolutions of a Digimon
    
    Args:
        digimon_name: Name of the Digimon
        
    Returns:
        List of post-evolutions
    """
    if service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        result = service.get_evolution_line_dict(digimon_name)
        
        # Check if there's an error
        if 'error' in result and result['error']:
            raise HTTPException(status_code=404, detail=result['message'])
        
        next_evolutions = result['postEvolutions']
        
        return {
            "digimon": digimon_name,
            "total": len(next_evolutions),
            "evolutions": next_evolutions
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/evolution/{digimon_name}/previous", tags=["Evolution"])
async def get_previous_evolutions(digimon_name: str):
    """
    Get only pre-evolutions of a Digimon
    
    Args:
        digimon_name: Name of the Digimon
        
    Returns:
        List of pre-evolutions
    """
    if service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        result = service.get_evolution_line_dict(digimon_name)
        
        # Check if there's an error
        if 'error' in result and result['error']:
            raise HTTPException(status_code=404, detail=result['message'])
        
        previous_evolutions = result['preEvolutions']
        
        return {
            "digimon": digimon_name,
            "total": len(previous_evolutions),
            "evolutions": previous_evolutions
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/evolution/{digimon_name}/summary", tags=["Evolution"])
async def get_evolution_summary(digimon_name: str):
    """
    Get evolution summary for a Digimon
    
    Args:
        digimon_name: Name of the Digimon
        
    Returns:
        Summary with evolution counts
    """
    if service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        result = service.get_evolution_line_dict(digimon_name)
        
        # Check if there's an error
        if 'error' in result and result['error']:
            raise HTTPException(status_code=404, detail=result['message'])
        
        return {
            "digimon": {
                "name": result['currentDigimon']['name'],
                "stage": result['currentDigimon']['stage'],
                "attribute": result['currentDigimon']['attribute']
            },
            "summary": {
                "total_pre_evolutions": len(result['preEvolutions']),
                "total_post_evolutions": len(result['postEvolutions'])
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/can-evolve/{from_digimon}/{to_digimon}", tags=["Evolution"])
async def can_evolve(from_digimon: str, to_digimon: str):
    """
    Check if a Digimon can evolve into another
    
    Args:
        from_digimon: Source Digimon
        to_digimon: Target Digimon
        
    Returns:
        Result indicating if direct evolution is possible
    """
    if service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        result = service.get_evolution_line_dict(from_digimon)
        
        # Check if there's an error
        if 'error' in result and result['error']:
            raise HTTPException(status_code=404, detail=f"Digimon not found: {from_digimon}")
        
        next_evolutions = result['postEvolutions']
        evolution_names = [evo['name'].lower() for evo in next_evolutions]
        
        can_evolve_to = to_digimon.lower() in evolution_names
        
        return {
            "from": from_digimon,
            "to": to_digimon,
            "can_evolve": can_evolve_to,
            "message": f"{from_digimon} {'can' if can_evolve_to else 'cannot'} evolve directly into {to_digimon}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.environ.get("PORT", 8000))
    
    print("\n🚀 Starting Digimon Evolution API...")
    print(f"📚 Documentation available at: http://localhost:{port}/docs")
    print(f"🔗 API available at: http://localhost:{port}\n")
    
    uvicorn.run(app, host="0.0.0.0", port=port)