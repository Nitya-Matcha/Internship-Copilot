interface Props {

    job: {

        company: string;
        title: string;
        location?: string;
        url: string;

        match_score: number;

        reason: string;

        missing_skills: string[];

    };


    markApplied: (job: {
        company:string;
        title:string;
        url:string;
    }) => void;

}



export default function InternshipCard({
    job,
    markApplied
}: Props) {


    return (

        <div className="bg-white rounded-xl shadow-md p-6">


            <h3 className="text-xl font-bold">
                {job.title}
            </h3>


            <p className="text-gray-700">
                {job.company}
            </p>


            {
                job.location && (

                    <p className="text-gray-500">
                        {job.location}
                    </p>

                )
            }



            <p className="mt-3">

                Match Score:

                <span className="font-bold ml-2">
                    {job.match_score}%
                </span>

            </p>




            <p className="mt-3">
                {job.reason}
            </p>



            {
                (job.missing_skills || []).length > 0 && (

                    <div className="mt-3">

                        <p className="font-semibold">
                            Missing Skills:
                        </p>


                        <ul className="list-disc ml-5">

                            {
                                job.missing_skills.map(
                                    (skill, index) => (

                                        <li key={index}>
                                            {skill}
                                        </li>

                                    )
                                )
                            }

                        </ul>

                    </div>

                )
            }




            <div className="mt-5">


                <a
                    href={job.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-4 py-2 rounded-lg bg-blue-600 text-white"
                >
                    Apply Here
                </a>



                <button

                    onClick={() => markApplied(job)}

                    className="ml-3 px-4 py-2 rounded-lg bg-green-600 text-white"

                >
                    Applied
                </button>


            </div>


        </div>

    );

}