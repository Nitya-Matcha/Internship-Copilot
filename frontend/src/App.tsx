import { useState } from "react";
import axios from "axios";
import InternshipCard from "./components/InternshipCard";

function App() {

    const [file, setFile] = useState<File | null>(null);
    const [matches, setMatches] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [applying, setApplying] = useState(false);
    const [error, setError] = useState("");


    async function getMatches() {

        if (!file) {
            return;
        }


        const formData = new FormData();

        formData.append(
            "file",
            file
        );


        const response = await axios.post(
            "http://127.0.0.1:8000/ai-match",
            formData,
            {
                headers:{
                    "Content-Type":"multipart/form-data",
                },
            }
        );


        setMatches(
            response.data.matches || []
        );

    }



    async function uploadResume() {

        if (!file) {
            setError("Please select a resume first.");
            return;
        }


        setLoading(true);
        setError("");


        try {

            await getMatches();


        } catch(err) {

            console.error(err);
            setError("Failed to analyze resume.");

        } finally {

            setLoading(false);

        }

    }



    async function markApplied(job:any) {


        try {

            setApplying(true);


            // Save application
            await axios.post(
                "http://127.0.0.1:8000/apply",
                {
                    
                    company: job.company,
                    title: job.title,
                    url: job.url
                }
            );



            // Immediately remove card
            setMatches((previous)=> 
                previous.filter(
                    (item)=>item.url !== job.url
                )
            );



            // Generate replacement internship
            await getMatches();



        } catch(err) {

            console.error(err);
            alert("Failed to save application.");

        } finally {

            setApplying(false);

        }

    }



    return (

        <div className="min-h-screen bg-gray-100 p-8">

            <div className="max-w-5xl mx-auto">


                <h1 className="text-4xl font-bold mb-6">
                    Internship Copilot
                </h1>



                <div className="bg-white p-6 rounded-xl shadow-md">


                    <input

                        type="file"

                        accept=".pdf"

                        onChange={(e)=>{

                            if(e.target.files?.[0]){

                                setFile(
                                    e.target.files[0]
                                );

                            }

                        }}

                    />



                    <button

                        onClick={uploadResume}

                        disabled={loading}

                        className="ml-4 px-5 py-2 rounded-lg bg-black text-white disabled:opacity-50"

                    >

                        {
                            loading
                            ?
                            "Analyzing..."
                            :
                            "Analyze Resume"
                        }


                    </button>



                    {
                        error && (

                            <p className="text-red-500 mt-3">
                                {error}
                            </p>

                        )
                    }



                </div>





                <div className="mt-8">


                    <h2 className="text-2xl font-bold mb-4">

                        Recommended Internships

                    </h2>




                    {
                        applying && (

                            <p className="text-blue-600 mb-3">

                                Finding your next match...

                            </p>

                        )
                    }




                    {
                        !loading && matches.length === 0 && (

                            <p className="text-gray-500">

                                Upload your resume to receive internship recommendations.

                            </p>

                        )
                    }





                    <div className="grid gap-4">


                        {
                            matches.map((job,index)=>(


                                <InternshipCard

                                    key={job.url || index}

                                    job={job}

                                    markApplied={markApplied}

                                />


                            ))
                        }


                    </div>


                </div>



            </div>


        </div>

    );

}


export default App;